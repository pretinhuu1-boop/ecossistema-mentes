# HEALTH CHECKS — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 18)

---

## Objetivo

Implementar **sistema centralizado de health checks** para todos os módulos do ecossistema, garantindo visibilidade imediata sobre o estado de saúde de cada componente (Redis, Celery, ChromaDB, Rastreador, Minerador, Orquestrador).

---

## Stack Técnica

### Motor (Python)
- **FastAPI** — API REST com endpoint `/health`
- **Redis** — Cache de status e métricas
- **Celery** — Execução de checks em background
- **Prometheus** — Exportação de métricas de health
- **APScheduler** — Agendamento de checks periódicos

### Integração
- **Rastreador** → Check de conectividade e coleta
- **Minerador** → Check de processamento e LLMs
- **Orquestrador** → Check de filas e workers
- **ChromaDB** → Check de vector store
- **Redis** → Check de broker e cache
- **Celery** → Check de tasks e workers

---

## Funcionalidades

### Core
- [ ] Verificação de saúde de todos os módulos
- [ ] Status geral (healthy/unhealthy/degraded)
- [ ] Endpoint `/health` com detalhes
- [ ] Logs detalhados de cada check
- [ ] Alertas quando algo fica unhealthy
- [ ] Histórico de checks
- [ ] Métricas Prometheus

### Checks por Módulo
- [ ] **Redis** — Conectividade, latência, memória, conexões
- [ ] **Celery** — Workers ativos, filas, tasks pendentes, heartbeat
- [ ] **ChromaDB** — Conectividade, coleções, storage
- [ ] **Rastreador** — Disponibilidade, última coleta, erros
- [ ] **Minerador** — Disponibilidade, última extração, API LLMs
- [ ] **Orquestrador** — Filas, workers, eventos

### Níveis de Status
- **HEALTHY** — Todos os checks passaram
- **DEGRADED** — Alguns checks falharam mas sistema operacional
- **UNHEALTHY** — Crítico, sistema não funcional

### Logs
- [ ] Timestamp de cada check
- [ ] Duração do check
- [ ] Resultado (pass/fail)
- [ ] Mensagem de erro (se aplicável)
- [ ] Métricas coletadas
- [ ] Armazenamento rotativo (últimos 30 dias)

### Alertas
- [ ] Alerta ao transicionar para UNHEALTHY
- [ ] Alerta ao transicionar para DEGRADED
- [ ] Alerta de recuperação (UNHEALTHY → HEALTHY)
- [ ] Canais: Telegram, Slack, Email
- [ ] Deduplication (evita spam)

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                   HEALTH CHECK ENGINE                    │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ SCHEDULER   │  │ CHECKER     │  │ ALERTER     │    │
│  │ (APScheduler) │  │ (Executor)  │  │ (Notifier)  │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │            │
│         ▼                ▼                ▼            │
│  ┌──────────────────────────────────────────────┐      │
│  │         CHECK RUNNERS (por módulo)          │      │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       │      │
│  │  │Redis │ │Celery│ │Chroma│ │Rast  │ ...  │      │
│  │  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘       │      │
│  └─────┼────────┼────────┼────────┼────────────┘      │
│        │        │        │        │                   │
│        ▼        ▼        ▼        ▼                   │
│  ┌──────────────────────────────────────────────┐      │
│  │           STATUS AGGREGATOR                   │      │
│  │      (Calcula status geral)                  │      │
│  └──────────────────┬───────────────────────────┘      │
│                     │                                 │
│         ┌───────────┼───────────┐                      │
│         ▼           ▼           ▼                      │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐               │
│  │  /health │ │  Redis  │ │Prometheus│               │
│  │  API     │ │  Cache   │ │ Metrics  │               │
│  └──────────┘ └─────────┘ └──────────┘               │
└─────────────────────────────────────────────────────────┘
```

---

## Estrutura de Check

### Resultado de Check
```python
@dataclass
class HealthCheckResult:
    """Resultado de um health check"""
    module: str                    # Nome do módulo
    status: Literal["pass", "fail", "warn"]
    duration_ms: float             # Tempo de execução
    timestamp: datetime
    message: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

@dataclass
class HealthStatus:
    """Status geral de saúde do sistema"""
    status: Literal["healthy", "degraded", "unhealthy"]
    timestamp: datetime
    checks: Dict[str, HealthCheckResult]
    summary: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    warned_checks: int
```

---

## Implementação: Health Check Engine

### 1. Health Checker Base
```python
"""
Health Check Engine
===================
Sistema centralizado de verificação de saúde dos módulos.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Dict, Any, Optional, List
from enum import Enum
import time
import redis
import celery
from chromadb import Client as ChromaClient
import logging

logger = logging.getLogger(__name__)


class HealthStatus(str, Enum):
    """Status de saúde"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class CheckStatus(str, Enum):
    """Status de um check individual"""
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


@dataclass
class HealthCheckResult:
    """Resultado de um health check"""
    module: str
    status: CheckStatus
    duration_ms: float
    timestamp: datetime
    message: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "module": self.module,
            "status": self.status.value,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "metrics": self.metrics,
            "error": self.error
        }


@dataclass
class SystemHealth:
    """Status geral de saúde do sistema"""
    status: HealthStatus
    timestamp: datetime
    checks: Dict[str, HealthCheckResult]
    summary: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    warned_checks: int

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "summary": self.summary,
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "warned_checks": self.warned_checks,
            "checks": {
                name: result.to_dict()
                for name, result in self.checks.items()
            }
        }


class BaseHealthChecker:
    """Base para health checkers de módulos"""

    def __init__(self, module_name: str, config: Dict[str, Any] = None):
        self.module_name = module_name
        self.config = config or {}
        self.logger = logging.getLogger(f"health.{module_name}")

    def check(self) -> HealthCheckResult:
        """Executa o check"""
        start_time = time.time()

        try:
            self.logger.info(f"Running health check for {self.module_name}")
            metrics = self._execute_check()

            # Determina status baseado nas métricas
            status, message = self._evaluate_status(metrics)

            duration_ms = (time.time() - start_time) * 1000

            result = HealthCheckResult(
                module=self.module_name,
                status=status,
                duration_ms=duration_ms,
                timestamp=datetime.utcnow(),
                message=message,
                metrics=metrics
            )

            self.logger.info(f"Check {self.module_name}: {status.value} ({duration_ms:.2f}ms)")
            return result

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.logger.error(f"Check {self.module_name} failed: {e}", exc_info=True)

            return HealthCheckResult(
                module=self.module_name,
                status=CheckStatus.FAIL,
                duration_ms=duration_ms,
                timestamp=datetime.utcnow(),
                message=f"Check failed with exception",
                error=str(e)
            )

    def _execute_check(self) -> Dict[str, Any]:
        """Executa a lógica do check (override em subclasses)"""
        raise NotImplementedError

    def _evaluate_status(self, metrics: Dict[str, Any]) -> tuple[CheckStatus, str]:
        """Avalia status baseado nas métricas (override em subclasses)"""
        return CheckStatus.PASS, "OK"


class HealthCheckEngine:
    """Engine central de health checks"""

    def __init__(self, redis_url: str = "redis://localhost:6379/4"):
        self.redis = redis.from_url(redis_url)
        self.checkers: Dict[str, BaseHealthChecker] = {}
        self.logger = logging.getLogger("health.engine")

        # Thresholds
        self.degraded_threshold = 0.3  # 30% fails = degraded
        self.unhealthy_threshold = 0.6  # 60% fails = unhealthy

    def register_checker(self, checker: BaseHealthChecker):
        """Registra um checker"""
        self.checkers[checker.module_name] = checker
        self.logger.info(f"Registered checker: {checker.module_name}")

    async def run_all_checks(self) -> SystemHealth:
        """Executa todos os checks registrados"""
        start_time = datetime.utcnow()
        results = {}

        for name, checker in self.checkers.items():
            try:
                results[name] = checker.check()
            except Exception as e:
                self.logger.error(f"Error running checker {name}: {e}", exc_info=True)
                results[name] = HealthCheckResult(
                    module=name,
                    status=CheckStatus.FAIL,
                    duration_ms=0,
                    timestamp=start_time,
                    message=f"Checker execution failed",
                    error=str(e)
                )

        # Calcula status geral
        status, summary = self._calculate_status(results)

        total = len(results)
        passed = sum(1 for r in results.values() if r.status == CheckStatus.PASS)
        failed = sum(1 for r in results.values() if r.status == CheckStatus.FAIL)
        warned = sum(1 for r in results.values() if r.status == CheckStatus.WARN)

        health = SystemHealth(
            status=status,
            timestamp=start_time,
            checks=results,
            summary=summary,
            total_checks=total,
            passed_checks=passed,
            failed_checks=failed,
            warned_checks=warned
        )

        # Salva no Redis
        await self._save_status(health)

        # Verifica transições de status
        await self._check_status_transitions(health)

        return health

    def _calculate_status(self, results: Dict[str, HealthCheckResult]) -> tuple[HealthStatus, str]:
        """Calcula status geral baseado nos resultados"""
        if not results:
            return HealthStatus.UNHEALTHY, "No checks available"

        total = len(results)
        failed = sum(1 for r in results.values() if r.status == CheckStatus.FAIL)
        warned = sum(1 for r in results.values() if r.status == CheckStatus.WARN)

        fail_rate = failed / total

        if fail_rate >= self.unhealthy_threshold:
            return HealthStatus.UNHEALTHY, f"{failed}/{total} checks failed"
        elif fail_rate >= self.degraded_threshold or warned > 0:
            return HealthStatus.DEGRADED, f"{failed} failed, {warned} warnings"
        else:
            return HealthStatus.HEALTHY, "All systems operational"

    async def _save_status(self, health: SystemHealth):
        """Salva status no Redis"""
        key = "health:status:current"

        try:
            self.redis.setex(
                key,
                300,  # 5 minutos TTL
                health.status.value
            )

            # Salva detalhes
            self.redis.setex(
                "health:status:details",
                300,
                str(health.to_dict())
            )

            # Salva histórico (últimos 100 checks)
            history_key = "health:history"
            self.redis.lpush(history_key, health.to_dict())
            self.redis.ltrim(history_key, 0, 99)

        except Exception as e:
            self.logger.error(f"Error saving status to Redis: {e}", exc_info=True)

    async def _check_status_transitions(self, health: SystemHealth):
        """Verifica transições de status e dispara alertas"""
        prev_status = self.redis.get("health:status:previous")

        if prev_status:
            prev_status = prev_status.decode()
            curr_status = health.status.value

            # Transição para UNHEALTHY
            if prev_status != "unhealthy" and curr_status == "unhealthy":
                await self._send_alert(
                    alert_type="status_unhealthy",
                    severity="critical",
                    message=f"🚨 System became UNHEALTHY: {health.summary}"
                )

            # Transição para DEGRADED
            elif prev_status not in ["degraded", "unhealthy"] and curr_status == "degraded":
                await self._send_alert(
                    alert_type="status_degraded",
                    severity="warning",
                    message=f"⚠️ System became DEGRADED: {health.summary}"
                )

            # Recuperação
            elif prev_status in ["degraded", "unhealthy"] and curr_status == "healthy":
                await self._send_alert(
                    alert_type="status_recovered",
                    severity="info",
                    message=f"✅ System recovered to HEALTHY"
                )

        # Atualiza status anterior
        self.redis.setex("health:status:previous", 3600, health.status.value)

    async def _send_alert(self, alert_type: str, severity: str, message: str):
        """Envia alerta (implementado separadamente)"""
        self.logger.warning(f"[ALERT {severity.upper()}] {message}")

        # Pub/Sub no Redis para alert manager consumir
        try:
            self.redis.publish("health:alerts", {
                "type": alert_type,
                "severity": severity,
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
            })
        except Exception as e:
            self.logger.error(f"Error publishing alert: {e}", exc_info=True)

    def get_current_status(self) -> Optional[str]:
        """Retorna status atual do cache"""
        try:
            status = self.redis.get("health:status:current")
            return status.decode() if status else None
        except Exception:
            return None
```

---

## Implementação: Checkers Específicos

### 2. Redis Health Checker
```python
class RedisHealthChecker(BaseHealthChecker):
    """Health checker para Redis"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("redis", config)
        self.redis_client = redis.from_url(
            config.get("redis_url", "redis://localhost:6379/0")
        )
        self.max_latency_ms = config.get("max_latency_ms", 100)
        self.max_memory_percent = config.get("max_memory_percent", 90)

    def _execute_check(self) -> Dict[str, Any]:
        """Executa check do Redis"""
        # Ping
        start = time.time()
        ping_result = self.redis_client.ping()
        latency_ms = (time.time() - start) * 1000

        # Info
        info = self.redis_client.info()

        # Memory
        used_memory = info.get("used_memory", 0)
        max_memory = info.get("maxmemory", 0)
        memory_percent = (used_memory / max_memory * 100) if max_memory > 0 else 0

        # Connections
        connected_clients = info.get("connected_clients", 0)

        # Uptime
        uptime_seconds = info.get("uptime_in_seconds", 0)

        # Teste de write/read
        test_key = "health:check:test"
        self.redis_client.setex(test_key, 10, "test")
        read_result = self.redis_client.get(test_key)
        write_ok = read_result == b"test"

        return {
            "ping": ping_result,
            "latency_ms": round(latency_ms, 2),
            "used_memory_bytes": used_memory,
            "max_memory_bytes": max_memory,
            "memory_percent": round(memory_percent, 2),
            "connected_clients": connected_clients,
            "uptime_seconds": uptime_seconds,
            "write_read_ok": write_ok
        }

    def _evaluate_status(self, metrics: Dict[str, Any]) -> tuple[CheckStatus, str]:
        """Avalia status do Redis"""
        if not metrics.get("ping"):
            return CheckStatus.FAIL, "Redis not responding"

        if not metrics.get("write_read_ok"):
            return CheckStatus.FAIL, "Redis write/read failed"

        latency = metrics.get("latency_ms", 0)
        if latency > self.max_latency_ms * 2:
            return CheckStatus.FAIL, f"Redis latency too high: {latency}ms"
        elif latency > self.max_latency_ms:
            return CheckStatus.WARN, f"Redis latency elevated: {latency}ms"

        memory_percent = metrics.get("memory_percent", 0)
        if memory_percent > self.max_memory_percent:
            return CheckStatus.WARN, f"Redis memory usage high: {memory_percent}%"

        return CheckStatus.PASS, f"Redis OK ({metrics['connected_clients']} clients)"
```

### 3. Celery Health Checker
```python
class CeleryHealthChecker(BaseHealthChecker):
    """Health checker para Celery"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("celery", config)
        self.celery_app = config.get("celery_app")
        self.min_workers = config.get("min_workers", 1)
        self.max_pending = config.get("max_pending", 1000)
        self.redis_client = redis.from_url(
            config.get("redis_url", "redis://localhost:6379/0")
        )

    def _execute_check(self) -> Dict[str, Any]:
        """Executa check do Celery"""
        # Workers ativos
        inspect = self.celery_app.control.inspect()
        active_workers = inspect.active() or {}
        stats = inspect.stats() or {}
        registered_tasks = inspect.registered() or {}

        worker_count = len(active_workers)
        active_tasks = sum(len(tasks) for tasks in active_workers.values())

        # Filas
        queue_metrics = {}
        for queue_name in self.celery_app.conf.task_queues:
            queue_name = queue_name.name if hasattr(queue_name, 'name') else queue_name
            pending = self.redis_client.llen(f"celery:queue:{queue_name}")
            reserved = self.redis_client.scard(f"celery:reserved:{queue_name}")
            queue_metrics[queue_name] = {
                "pending": pending,
                "reserved": reserved,
                "total": pending + reserved
            }

        # Stats do broker
        broker_latency = self._check_broker_latency()

        # Heartbeat
        last_heartbeat = self.redis_client.get("celery:last_heartbeat")
        heartbeat_age = None
        if last_heartbeat:
            heartbeat_age = (time.time() - float(last_heartbeat))

        return {
            "worker_count": worker_count,
            "active_tasks": active_tasks,
            "registered_tasks_count": len(registered_tasks),
            "queues": queue_metrics,
            "broker_latency_ms": broker_latency,
            "heartbeat_age_seconds": heartbeat_age,
            "workers": {
                name: {
                    "active_tasks": len(tasks),
                    "stats": stats.get(name, {})
                }
                for name, tasks in active_workers.items()
            }
        }

    def _check_broker_latency(self) -> float:
        """Verifica latência do broker"""
        start = time.time()
        try:
            self.redis_client.ping()
            return (time.time() - start) * 1000
        except Exception:
            return -1

    def _evaluate_status(self, metrics: Dict[str, Any]) -> tuple[CheckStatus, str]:
        """Avalia status do Celery"""
        worker_count = metrics.get("worker_count", 0)

        if worker_count == 0:
            return CheckStatus.FAIL, "No active Celery workers"

        if worker_count < self.min_workers:
            return CheckStatus.WARN, f"Only {worker_count} workers (min: {self.min_workers})"

        # Verifica total de pending
        total_pending = sum(
            q["pending"] for q in metrics.get("queues", {}).values()
        )
        if total_pending > self.max_pending:
            return CheckStatus.WARN, f"Too many pending tasks: {total_pending}"

        # Verifica heartbeat
        heartbeat_age = metrics.get("heartbeat_age_seconds")
        if heartbeat_age and heartbeat_age > 300:  # 5 minutos
            return CheckStatus.FAIL, f"No worker heartbeat for {heartbeat_age}s"

        return CheckStatus.PASS, f"Celery OK ({worker_count} workers, {total_pending} pending)"
```

### 4. ChromaDB Health Checker
```python
class ChromaHealthChecker(BaseHealthChecker):
    """Health checker para ChromaDB"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("chromadb", config)
        self.chroma_client = ChromaClient(
            host=config.get("host", "localhost"),
            port=config.get("port", 8000)
        )
        self.min_collections = config.get("min_collections", 0)

    def _execute_check(self) -> Dict[str, Any]:
        """Executa check do ChromaDB"""
        start = time.time()

        # Lista coleções
        collections = self.chroma_client.list_collections()

        # Conta embeddings
        total_embeddings = 0
        for collection in collections:
            count = collection.count()
            total_embeddings += count

        latency_ms = (time.time() - start) * 1000

        # Teste de query
        test_ok = False
        if collections:
            try:
                results = collections[0].query(
                    query_embeddings=[[0] * 384],  # Dummy embedding
                    n_results=1
                )
                test_ok = True
            except Exception:
                test_ok = False

        return {
            "collection_count": len(collections),
            "total_embeddings": total_embeddings,
            "latency_ms": round(latency_ms, 2),
            "test_query_ok": test_ok,
            "collections": [
                {
                    "name": c.name,
                    "count": c.count()
                }
                for c in collections[:10]  # Primeiras 10
            ]
        }

    def _evaluate_status(self, metrics: Dict[str, Any]) -> tuple[CheckStatus, str]:
        """Avalia status do ChromaDB"""
        collection_count = metrics.get("collection_count", 0)

        if self.min_collections > 0 and collection_count == 0:
            return CheckStatus.WARN, f"No collections found (min: {self.min_collections})"

        latency = metrics.get("latency_ms", 0)
        if latency > 5000:  # 5 segundos
            return CheckStatus.FAIL, f"ChromaDB latency too high: {latency}ms"

        if not metrics.get("test_query_ok") and collection_count > 0:
            return CheckStatus.WARN, "ChromaDB test query failed"

        return CheckStatus.PASS, f"ChromaDB OK ({collection_count} collections, {metrics['total_embeddings']} embeddings)"
```

### 5. Rastreador Health Checker
```python
class RastreadorHealthChecker(BaseHealthChecker):
    """Health checker para Rastreador"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("rastreador", config)
        self.redis_client = redis.from_url(
            config.get("redis_url", "redis://localhost:6379/0")
        )
        self.max_error_rate = config.get("max_error_rate", 0.1)  # 10%

    def _execute_check(self) -> Dict[str, Any]:
        """Executa check do Rastreador"""
        # Última coleta
        last_collection = self.redis_client.get("rastreador:last_collection")
        last_collection_age = None
        if last_collection:
            last_collection_age = (time.time() - float(last_collection))

        # Contadores
        collections_total = int(self.redis_client.get("rastreador:collections:total") or 0)
        collections_failed = int(self.redis_client.get("rastreador:collections:failed") or 0)

        # Taxa de erro
        error_rate = collections_failed / collections_total if collections_total > 0 else 0

        # Workers ativos
        active_collectors = self.redis_client.scard("rastreador:active_workers")

        # Status da fila
        queue_size = self.redis_client.llen("queue:rastreador")

        return {
            "last_collection_age_seconds": last_collection_age,
            "collections_total": collections_total,
            "collections_failed": collections_failed,
            "error_rate": round(error_rate, 4),
            "active_collectors": active_collectors,
            "queue_size": queue_size,
            "uptime_ok": last_collection_age is not None and last_collection_age < 3600
        }

    def _evaluate_status(self, metrics: Dict[str, Any]) -> tuple[CheckStatus, str]:
        """Avalia status do Rastreador"""
        error_rate = metrics.get("error_rate", 0)

        if error_rate > self.max_error_rate * 2:
            return CheckStatus.FAIL, f"Error rate too high: {error_rate:.2%}"
        elif error_rate > self.max_error_rate:
            return CheckStatus.WARN, f"Elevated error rate: {error_rate:.2%}"

        if not metrics.get("uptime_ok"):
            return CheckStatus.WARN, "No recent collections"

        return CheckStatus.PASS, f"Rastreador OK ({metrics['collections_total']} collections, {error_rate:.2%} errors)"
```

### 6. Minerador Health Checker
```python
class MineradorHealthChecker(BaseHealthChecker):
    """Health checker para Minerador"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("minerador", config)
        self.redis_client = redis.from_url(
            config.get("redis_url", "redis://localhost:6379/0")
        )
        self.llm_client = config.get("llm_client")
        self.max_error_rate = config.get("max_error_rate", 0.1)

    def _execute_check(self) -> Dict[str, Any]:
        """Executa check do Minerador"""
        # Última extração
        last_extraction = self.redis_client.get("minerador:last_extraction")
        last_extraction_age = None
        if last_extraction:
            last_extraction_age = (time.time() - float(last_extraction))

        # Contadores
        extractions_total = int(self.redis_client.get("minerador:extractions:total") or 0)
        extractions_failed = int(self.redis_client.get("minerador:extractions:failed") or 0)
        artifacts_created = int(self.redis_client.get("minerador:artifacts:total") or 0)

        # Taxa de erro
        error_rate = extractions_failed / extractions_total if extractions_total > 0 else 0

        # Workers ativos
        active_workers = self.redis_client.scard("minerador:active_workers")

        # Status da fila
        queue_size = self.redis_client.llen("queue:minerador")

        # Teste de API LLM
        llm_ok = False
        llm_latency_ms = 0
        if self.llm_client:
            try:
                start = time.time()
                response = self.llm_client.generate(
                    prompt="Test",
                    max_tokens=1
                )
                llm_latency_ms = (time.time() - start) * 1000
                llm_ok = True
            except Exception:
                llm_ok = False

        return {
            "last_extraction_age_seconds": last_extraction_age,
            "extractions_total": extractions_total,
            "extractions_failed": extractions_failed,
            "artifacts_created": artifacts_created,
            "error_rate": round(error_rate, 4),
            "active_workers": active_workers,
            "queue_size": queue_size,
            "llm_api_ok": llm_ok,
            "llm_latency_ms": round(llm_latency_ms, 2),
            "uptime_ok": last_extraction_age is not None and last_extraction_age < 3600
        }

    def _evaluate_status(self, metrics: Dict[str, Any]) -> tuple[CheckStatus, str]:
        """Avalia status do Minerador"""
        error_rate = metrics.get("error_rate", 0)

        if error_rate > self.max_error_rate * 2:
            return CheckStatus.FAIL, f"Error rate too high: {error_rate:.2%}"
        elif error_rate > self.max_error_rate:
            return CheckStatus.WARN, f"Elevated error rate: {error_rate:.2%}"

        if not metrics.get("llm_api_ok"):
            return CheckStatus.FAIL, "LLM API not responding"

        if not metrics.get("uptime_ok"):
            return CheckStatus.WARN, "No recent extractions"

        llm_latency = metrics.get("llm_latency_ms", 0)
        if llm_latency > 10000:  # 10 segundos
            return CheckStatus.WARN, f"LLM API slow: {llm_latency}ms"

        return CheckStatus.PASS, f"Minerador OK ({metrics['artifacts_created']} artifacts, {llm_latency:.0f}ms latency)"
```

### 7. Orquestrador Health Checker
```python
class OrquestradorHealthChecker(BaseHealthChecker):
    """Health checker para Orquestrador"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("orquestrador", config)
        self.redis_client = redis.from_url(
            config.get("redis_url", "redis://localhost:6379/0")
        )
        self.celery_app = config.get("celery_app")

    def _execute_check(self) -> Dict[str, Any]:
        """Executa check do Orquestrador"""
        # Eventos recentes
        recent_events = self.redis_client.lrange("events:recent", 0, 9)
        last_event_age = None
        if recent_events:
            import json
            last_event = json.loads(recent_events[0])
            last_event_age = (time.time() - last_event.get("timestamp", 0))

        # Contadores de eventos
        events_total = int(self.redis_client.get("events:total") or 0)
        events_failed = int(self.redis_client.get("events:failed") or 0)

        # Status das filas
        queues = {}
        for queue_name in ["high", "normal", "low"]:
            pending = self.redis_client.llen(f"queue:orchestrator:{queue_name}")
            queues[queue_name] = {"pending": pending}

        # Workers
        inspect = self.celery_app.control.inspect()
        active_workers = inspect.active() or {}

        return {
            "last_event_age_seconds": last_event_age,
            "events_total": events_total,
            "events_failed": events_failed,
            "queues": queues,
            "worker_count": len(active_workers),
            "events_ok": last_event_age is not None and last_event_age < 300  # 5 minutos
        }

    def _evaluate_status(self, metrics: Dict[str, Any]) -> tuple[CheckStatus, str]:
        """Avalia status do Orquestrador"""
        worker_count = metrics.get("worker_count", 0)

        if worker_count == 0:
            return CheckStatus.FAIL, "No active Orquestrador workers"

        if not metrics.get("events_ok"):
            return CheckStatus.WARN, "No recent events"

        # Verifica filas
        total_pending = sum(
            q["pending"] for q in metrics.get("queues", {}).values()
        )
        if total_pending > 1000:
            return CheckStatus.WARN, f"Orchestrator backlog: {total_pending} tasks"

        return CheckStatus.PASS, f"Orquestrador OK ({worker_count} workers, {total_pending} pending)"
```

---

## Implementação: API FastAPI

### 8. FastAPI Health Endpoint
```python
"""
FastAPI Health Check Endpoint
==============================
Endpoint /health para consulta de status do sistema.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import asyncio
from typing import Optional

app = FastAPI(title="Health Checks API", version="1.0.0")

# Engine global
health_engine: Optional[HealthCheckEngine] = None


def init_health_engine(engine: HealthCheckEngine):
    """Inicializa engine de health checks"""
    global health_engine
    health_engine = engine


@app.get("/health")
async def get_health():
    """Retorna status atual de saúde do sistema"""
    if not health_engine:
        raise HTTPException(status_code=503, detail="Health engine not initialized")

    health = await health_engine.run_all_checks()
    return JSONResponse(
        status_code=200 if health.status == HealthStatus.HEALTHY else 503,
        content=health.to_dict()
    )


@app.get("/health/status")
async def get_status():
    """Retorna apenas status geral (simplificado)"""
    if not health_engine:
        return {"status": "unknown", "message": "Health engine not initialized"}

    status = health_engine.get_current_status()
    return {
        "status": status or "unknown",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health/summary")
async def get_summary():
    """Retorna resumo dos checks"""
    if not health_engine:
        raise HTTPException(status_code=503, detail="Health engine not initialized")

    health = await health_engine.run_all_checks()

    return {
        "status": health.status.value,
        "summary": health.summary,
        "total_checks": health.total_checks,
        "passed_checks": health.passed_checks,
        "failed_checks": health.failed_checks,
        "warned_checks": health.warned_checks,
        "failed_modules": [
            name for name, result in health.checks.items()
            if result.status == CheckStatus.FAIL
        ],
        "warned_modules": [
            name for name, result in health.checks.items()
            if result.status == CheckStatus.WARN
        ]
    }


@app.get("/health/history")
async def get_history(limit: int = 10):
    """Retorna histórico de health checks"""
    if not health_engine:
        raise HTTPException(status_code=503, detail="Health engine not initialized")

    try:
        history = health_engine.redis.lrange("health:history", 0, limit - 1)
        return {
            "count": len(history),
            "history": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health/readiness")
async def get_readiness():
    """Kubernetes readiness probe"""
    if not health_engine:
        return {"ready": False}

    # Verifica componentes críticos apenas
    critical_checks = ["redis", "celery"]

    for check_name in critical_checks:
        if check_name not in health_engine.checkers:
            return {"ready": False, "reason": f"Missing check: {check_name}"}

        result = health_engine.checkers[check_name].check()
        if result.status == CheckStatus.FAIL:
            return {"ready": False, "reason": f"{check_name} is unhealthy"}

    return {"ready": True}


@app.get("/health/liveness")
async def get_liveness():
    """Kubernetes liveness probe"""
    return {"alive": True}


# Health check para a própria API
@app.get("/health/self")
async def get_self_health():
    """Health check da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

---

## Implementação: Agendador de Checks

### 9. Agendador Periódico
```python
"""
Periodic Health Check Scheduler
===============================
Agenda e executa health checks periodicamente.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger = logging.getLogger(__name__)


class HealthCheckScheduler:
    """Agendador de health checks periódicos"""

    def __init__(
        self,
        health_engine: HealthCheckEngine,
        check_interval_seconds: int = 60
    ):
        self.engine = health_engine
        self.check_interval = check_interval_seconds
        self.scheduler = AsyncIOScheduler()
        self.logger = logging.getLogger("health.scheduler")

    def start(self):
        """Inicia o agendador"""
        self.logger.info(f"Starting health check scheduler (interval: {self.check_interval}s)")

        # Agenda check periódico
        self.scheduler.add_job(
            self._run_periodic_check,
            trigger=IntervalTrigger(seconds=self.check_interval),
            id="periodic_health_check",
            replace_existing=True
        )

        self.scheduler.start()

    async def _run_periodic_check(self):
        """Executa check periódico"""
        try:
            self.logger.debug("Running periodic health check")
            health = await self.engine.run_all_checks()

            # Log baseado no status
            if health.status == HealthStatus.UNHEALTHY:
                self.logger.error(f"Health check: {health.status.value} - {health.summary}")
            elif health.status == HealthStatus.DEGRADED:
                self.logger.warning(f"Health check: {health.status.value} - {health.summary}")
            else:
                self.logger.info(f"Health check: {health.status.value}")

        except Exception as e:
            self.logger.error(f"Error in periodic health check: {e}", exc_info=True)

    def stop(self):
        """Para o agendador"""
        self.logger.info("Stopping health check scheduler")
        self.scheduler.shutdown()
```

---

## Implementação: Alert Manager

### 10. Alert Manager para Notificações
```python
"""
Alert Manager
=============
Gerencia alertas de health checks via Telegram, Slack e Email.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class AlertManager:
    """Gerenciador de alertas"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger("health.alerts")

        # Deduplication (evita spam)
        self.alert_history = {}
        self.dedup_window = timedelta(minutes=config.get("dedup_minutes", 5))

        # Canais
        self.telegram_enabled = config.get("telegram", {}).get("enabled", False)
        self.slack_enabled = config.get("slack", {}).get("enabled", False)
        self.email_enabled = config.get("email", {}).get("enabled", False)

    async def send_alert(self, alert_data: Dict[str, Any]):
        """Envia alerta para os canais configurados"""
        alert_type = alert_data.get("type")
        severity = alert_data.get("severity", "info")
        message = alert_data.get("message", "")

        # Deduplication
        if self._is_duplicate(alert_type, severity, message):
            self.logger.debug(f"Alert deduplicated: {alert_type}")
            return

        # Marca como enviado
        self._mark_sent(alert_type, severity, message)

        self.logger.warning(f"[ALERT {severity.upper()}] {message}")

        # Envia para canais baseado na severidade
        if severity == "critical":
            await self._send_all_channels(alert_data)
        elif severity == "warning":
            await self._send_telegram(alert_data)
            await self._send_slack(alert_data)
        else:  # info
            await self._send_telegram(alert_data)

    def _is_duplicate(self, alert_type: str, severity: str, message: str) -> bool:
        """Verifica se alerta é duplicado"""
        key = f"{alert_type}:{severity}:{message}"

        if key in self.alert_history:
            last_sent = self.alert_history[key]
            if datetime.utcnow() - last_sent < self.dedup_window:
                return True

        return False

    def _mark_sent(self, alert_type: str, severity: str, message: str):
        """Marca alerta como enviado"""
        key = f"{alert_type}:{severity}:{message}"
        self.alert_history[key] = datetime.utcnow()

        # Limpa histórico antigo
        self._cleanup_history()

    def _cleanup_history(self):
        """Limpa alertas antigos do histórico"""
        now = datetime.utcnow()
        self.alert_history = {
            k: v for k, v in self.alert_history.items()
            if now - v < self.dedup_window * 2
        }

    async def _send_all_channels(self, alert_data: Dict[str, Any]):
        """Envia para todos os canais"""
        await self._send_telegram(alert_data)
        await self._send_slack(alert_data)
        await self._send_email(alert_data)

    async def _send_telegram(self, alert_data: Dict[str, Any]):
        """Envia alerta via Telegram"""
        if not self.telegram_enabled:
            return

        try:
            # Integração com Telegram seria implementada aqui
            # Exemplo usando biblioteca python-telegram-bot
            self.logger.info(f"Telegram alert: {alert_data['message']}")
        except Exception as e:
            self.logger.error(f"Error sending Telegram alert: {e}", exc_info=True)

    async def _send_slack(self, alert_data: Dict[str, Any]):
        """Envia alerta via Slack"""
        if not self.slack_enabled:
            return

        try:
            # Integração com Slack seria implementada aqui
            # Exemplo usando biblioteca slack-sdk
            self.logger.info(f"Slack alert: {alert_data['message']}")
        except Exception as e:
            self.logger.error(f"Error sending Slack alert: {e}", exc_info=True)

    async def _send_email(self, alert_data: Dict[str, Any]):
        """Envia alerta via Email"""
        if not self.email_enabled:
            return

        try:
            # Integração com Email seria implementada aqui
            # Exemplo usando smtplib ou biblioteca sendgrid
            self.logger.info(f"Email alert: {alert_data['message']}")
        except Exception as e:
            self.logger.error(f"Error sending Email alert: {e}", exc_info=True)
```

---

## Integração com Prometheus

### 11. Prometheus Metrics Exporter
```python
"""
Prometheus Metrics Exporter
============================
Exporta métricas de health checks para Prometheus.
"""

from prometheus_client import Gauge, Counter, Histogram, start_http_server
import logging

logger = logging.getLogger(__name__)


class HealthCheckPrometheus:
    """Exportador de métricas Prometheus"""

    def __init__(self, port: int = 9091):
        self.port = port

        # Métricas
        self.health_status = Gauge(
            'health_check_status',
            'Health check status (1=healthy, 0.5=degraded, 0=unhealthy)',
            ['module']
        )

        self.health_check_duration = Histogram(
            'health_check_duration_seconds',
            'Health check duration',
            ['module']
        )

        self.health_check_total = Counter(
            'health_check_total',
            'Total health checks',
            ['module', 'status']
        )

        self.alerts_total = Counter(
            'health_alerts_total',
            'Total alerts sent',
            ['type', 'severity']
        )

        self.logger = logging.getLogger("health.prometheus")

    def start_server(self):
        """Inicia servidor Prometheus"""
        try:
            start_http_server(self.port)
            self.logger.info(f"Prometheus metrics server started on port {self.port}")
        except Exception as e:
            self.logger.error(f"Error starting Prometheus server: {e}", exc_info=True)

    def record_check(self, result: HealthCheckResult):
        """Registra resultado de check"""
        # Status numérico
        status_value = {
            CheckStatus.PASS: 1.0,
            CheckStatus.WARN: 0.5,
            CheckStatus.FAIL: 0.0
        }[result.status]

        # Atualiza gauge
        self.health_status.labels(module=result.module).set(status_value)

        # Registra duração
        self.health_check_duration.labels(
            module=result.module
        ).observe(result.duration_ms / 1000)

        # Incrementa contador
        self.health_check_total.labels(
            module=result.module,
            status=result.status.value
        ).inc()

    def record_alert(self, alert_type: str, severity: str):
        """Registra alerta enviado"""
        self.alerts_total.labels(
            type=alert_type,
            severity=severity
        ).inc()
```

---

## Integração e Setup Completo

### 12. Setup e Inicialização
```python
"""
Health Checks Setup
===================
Inicialização completa do sistema de health checks.
"""

import asyncio
import logging
from celery import Celery

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def setup_health_checks(
    redis_url: str = "redis://localhost:6379/0",
    celery_broker: str = "redis://localhost:6379/1",
    chroma_host: str = "localhost",
    chroma_port: int = 8000,
    llm_client = None
):
    """Configura sistema de health checks completo"""

    # Engine
    engine = HealthCheckEngine(redis_url=f"{redis_url}/4")

    # Configuração
    config = {
        "redis_url": redis_url,
        "celery_app": Celery(broker=celery_broker),
        "host": chroma_host,
        "port": chroma_port,
        "llm_client": llm_client,
        "max_latency_ms": 100,
        "max_memory_percent": 90,
        "min_workers": 1,
        "max_pending": 1000,
        "max_error_rate": 0.1
    }

    # Registra checkers
    engine.register_checker(RedisHealthChecker(config))
    engine.register_checker(CeleryHealthChecker(config))
    engine.register_checker(ChromaHealthChecker(config))
    engine.register_checker(RastreadorHealthChecker(config))
    engine.register_checker(MineradorHealthChecker(config))
    engine.register_checker(OrquestradorHealthChecker(config))

    # Prometheus
    prometheus = HealthCheckPrometheus(port=9091)
    prometheus.start_server()

    # Agendador
    scheduler = HealthCheckScheduler(engine, check_interval_seconds=60)
    scheduler.start()

    # API FastAPI
    init_health_engine(engine)

    logger.info("Health checks system initialized")

    return engine, scheduler, prometheus


async def main():
    """Função principal para testes"""
    from fastapi import FastAPI
    import uvicorn

    # Setup
    engine, scheduler, prometheus = setup_health_checks()

    # Roda um check inicial
    health = await engine.run_all_checks()
    logger.info(f"Initial health status: {health.status.value}")
    logger.info(f"Summary: {health.summary}")

    # Exibe detalhes
    for name, result in health.checks.items():
        status_icon = "✅" if result.status == CheckStatus.PASS else \
                     "⚠️" if result.status == CheckStatus.WARN else "❌"
        logger.info(f"  {status_icon} {name}: {result.message} ({result.duration_ms:.2f}ms)")

    # Inicia API
    app = FastAPI()
    app.mount("/health", app)
    uvicorn.run(app, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Comandos CLI

```bash
# Ver status de saúde atual
health-check status

# Executar checks completos
health-check check --all

# Executar check de módulo específico
health-check check --module redis
health-check check --module celery
health-check check --module chromadb
health-check check --module rastreador
health-check check --module minerador
health-check check --module orquestrador

# Ver histórico de checks
health-check history --limit 20

# Ver logs detalhados
health-check logs --module redis --tail 50

# Iniciar servidor de API
health-check api start --port 8001

# Iniciar agendador de checks periódicos
health-check scheduler start --interval 60

# Configurar alertas
health-check alerts configure --telegram
health-check alerts configure --slack
health-check alerts configure --email

# Testar alertas
health-check alerts test --type critical
health-check alerts test --type warning

# Ver métricas Prometheus
health-check metrics

# Ver detalhes de check específico
health-check inspect --module redis --timestamp 2026-01-31T12:00:00Z

# Exportar relatório
health-check report --format json --output health-report.json
health-check report --format html --output health-report.html
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Engine de health checks
- [ ] Checkers para Redis, Celery, ChromaDB
- [ ] Endpoint `/health` básico
- [ ] Status geral (healthy/unhealthy)
- [ ] Logs básicos

### v0.5
- [ ] Checkers para Rastreador, Minerador, Orquestrador
- [ ] Alertas por Telegram
- [ ] Agendador de checks periódicos
- [ ] Histórico de checks
- [ ] Deduplication de alertas

### v1.0
- [ ] Alertas por Slack e Email
- [ ] Métricas Prometheus
- [ ] Dashboards Grafana
- [ ] Kubernetes probes (readiness/liveness)
- [ ] Relatórios detalhados (JSON/HTML)
- [ ] Configuração customizável de thresholds
- [ ] Integração completa com Monitoramento

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 18*
