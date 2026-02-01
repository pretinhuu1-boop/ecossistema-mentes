# MONITORAMENTO — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 9)

---

## Problema

**Hoje:**
- Sistema roda automaticamente 24/7
- **Como saber se algo deu errado?**

**Precisamos de:**
- Sistema de monitoramento
- Alertas (email, Telegram, Slack)
- Dashboards de métricas em tempo real

---

## Stack Técnica

### Motor (Python)
- **Prometheus** — Coleta de métricas
- **Grafana** — Dashboards
- **Redis** — Cache de métricas

### Integração
- **Orquestrador** → Publica métricas
- **Monitor** → Coleta e alerta
- **Grafana** → Visualiza dashboards

---

## Funcionalidades

### Core
- [ ] Coleta métricas de todos os módulos
- [ ] Exibe dashboards em tempo real
- [ ] Envia alertas automaticamente
- [ ] Histórico de métricas

### Dashboards
- [ ] Status geral do sistema
- [ ] Filas (quantos tasks, quantos workers)
- [ ] Progresso do fluxo (onde tá cada fonte)
- [ ] Métricas de qualidade (cobertura, confidence, etc.)
- [ ] Erros e falhas

### Alertas
- [ ] Alertas por email
- [ ] Alertas por Telegram
- [ ] Alertas por Slack
- [ ] Níveis de urgência (info, warning, critical)

---

## Métricas Monitoradas

### 1. Filas
```yaml
filas:
  high:
    pending: Quantos tasks na fila
    processing: Quantos tasks rodando
    failed: Quantos tasks falharam
  normal:
    pending: ...
    processing: ...
    failed: ...
  low:
    pending: ...
    processing: ...
    failed: ...
```

### 2. Progresso do Fluxo
```yaml
progresso:
  sources_collected: Quantas fontes coletadas
  sources_failed: Quantas falhas na coleta
  artifacts_extracted: Quantos artefatos extraídos
  artifacts_failed: Quantas falhas na extração
  minds_built: Quantas mentes construídas
  total_sources: Total de fontes
  progress_percent: % completo
```

### 3. Qualidade
```yaml
qualidade:
  cobertura: % de fontes coletadas
  confidence: Média de confiança dos artefatos
  consistencia: % de artefatos consistentes
  gaps: Quantos gaps identificados
```

### 4. Erros
```yaml
erros:
  rastreador_errors: Erros do Rastreador
  minerador_errors: Erros do Minerador
  construtor_errors: Erros do Construtor
  orquestrador_errors: Erros do Orquestrador
```

---

## Coleta de Métricas

```python
class MetricsCollector:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=3)
        self.prometheus = PrometheusClient()

    def collect_queue_metrics(self):
        """Coleta métricas das filas"""
        from celery import current_app

        queues = current_app.conf.task_queues

        for queue in queues:
            # Pending
            pending = self.redis.llen(f"celery:queue:{queue.name}")
            self.prometheus.gauge(
                'queue_pending',
                pending,
                labels={'queue': queue.name}
            )

            # Processing
            processing = self.redis.scard(f"celery:reserved:{queue.name}")
            self.prometheus.gauge(
                'queue_processing',
                processing,
                labels={'queue': queue.name}
            )

            # Failed
            failed = self.redis.get(f"celery:failed:{queue.name}", 0)
            self.prometheus.gauge(
                'queue_failed',
                int(failed),
                labels={'queue': queue.name}
            )

    def collect_progress_metrics(self, project_name):
        """Coleta métricas de progresso"""
        from ..events import EventType
        from ..publisher import EventStore

        sources_collected = EventStore.count(EventType.SOURCE_COLLECTED, project_name)
        sources_failed = EventStore.count(EventType.SOURCE_FAILED, project_name)
        artifacts_extracted = EventStore.count(EventType.ARTIFACT_EXTRACTED, project_name)
        artifacts_failed = EventStore.count(EventType.ARTIFACT_FAILED, project_name)
        minds_built = EventStore.count(EventType.MIND_BUILT, project_name)

        self.prometheus.gauge(
            'progress_sources_collected',
            sources_collected,
            labels={'project': project_name}
        )

        self.prometheus.gauge(
            'progress_artifacts_extracted',
            artifacts_extracted,
            labels={'project': project_name}
        )

        # ... etc

    def collect_quality_metrics(self, project_name):
        """Coleta métricas de qualidade"""
        from ..estado import StateManager

        state = StateManager(project_name)
        metrics = state.get_metrics()

        self.prometheus.gauge(
            'quality_coverage',
            metrics['cobertura'],
            labels={'project': project_name}
        )

        self.prometheus.gauge(
            'quality_confidence',
            metrics['confidence'],
            labels={'project': project_name}
        )

        # ... etc
```

---

## Alertas

```python
class AlertManager:
    def __init__(self):
        self.telegram = TelegramClient()
        self.email = EmailClient()
        self.slack = SlackClient()

    def send_alert(self, alert):
        """Envia alerta"""
        urgency = alert["urgency"]

        # Critical: Todos os canais
        if urgency == "critical":
            self.telegram.send(alert)
            self.email.send(alert)
            self.slack.send(alert)

        # Warning: Telegram + Slack
        elif urgency == "warning":
            self.telegram.send(alert)
            self.slack.send(alert)

        # Info: Só Telegram
        elif urgency == "info":
            self.telegram.send(alert)

    def monitor_queues(self):
        """Monitora filas e alerta se necessário"""
        from .metrics import MetricsCollector

        collector = MetricsCollector()

        # Coleta métricas
        metrics = collector.collect_queue_metrics()

        # Verifica condições de alerta
        for queue_name, queue_metrics in metrics.items():
            # Se há muitos tasks na fila
            if queue_metrics["pending"] > 100:
                self.send_alert({
                    "type": "queue_backlog",
                    "queue": queue_name,
                    "pending": queue_metrics["pending"],
                    "message": f"⚠️ Fila {queue_name} com {queue_metrics['pending']} tasks pendentes",
                    "urgency": "warning"
                })

            # Se há muitos falhos
            if queue_metrics["failed"] > 10:
                self.send_alert({
                    "type": "queue_failed",
                    "queue": queue_name,
                    "failed": queue_metrics["failed"],
                    "message": f"🚨 Fila {queue_name} com {queue_metrics['failed']} tasks falhados",
                    "urgency": "critical"
                })

    def monitor_quality(self, project_name):
        """Monitora qualidade e alerta se necessário"""
        from .metrics import MetricsCollector

        collector = MetricsCollector()
        metrics = collector.collect_quality_metrics(project_name)

        # Verifica qualidade
        if metrics["confidence"] < 0.7:
            self.send_alert({
                "type": "quality_low",
                "project": project_name,
                "confidence": metrics["confidence"],
                "message": f"⚠️ Qualidade baixa: confidence {metrics['confidence']}",
                "urgency": "warning"
            })

        # ... etc
```

---

## Dashboards (Grafana)

### Dashboard 1: Status Geral
```
┌─────────────────────────────────────────────────┐
│  STATUS DO SISTEMA                               │
│                                                  │
│  🟢 Sistema Online                               │
│  📊 Filas                                       │
│     High: 5 pending, 2 processing               │
│     Normal: 15 pending, 5 processing             │
│     Low: 50 pending, 1 processing               │
│                                                  │
│  📈 Progresso                                    │
│     Fontes: 120/150 (80%)                        │
│     Artefatos: 300/350 (86%)                     │
│     Mentes: 1/1 (100%)                           │
│                                                  │
│  📊 Qualidade                                     │
│     Cobertura: 95% ✅                            │
│     Confidence: 0.86 ✅                         │
│     Consistência: 0.92 ✅                        │
└─────────────────────────────────────────────────┘
```

### Dashboard 2: Filas
```
┌─────────────────────────────────────────────────┐
│  FILAS                                          │
│                                                  │
│  HIGH PRIORITY                                  │
│  ┌─────┬─────┬─────┐                            │
│  │Pend │Proc │Fail │                            │
│  ├─────┼─────┼─────┤                            │
│  │  5  │  2  │  0  │                            │
│  └─────┴─────┴─────┘                            │
│                                                  │
│  NORMAL PRIORITY                                │
│  ┌─────┬─────┬─────┐                            │
│  │Pend │Proc │Fail │                            │
│  ├─────┼─────┼─────┤                            │
│  │ 15  │  5  │  1  │                            │
│  └─────┴─────┴─────┘                            │
└─────────────────────────────────────────────────┘
```

### Dashboard 3: Qualidade ao Longo do Tempo
```
[Gráfico de linha]

Qualidade (0-1)
 1.0 │                ╱───
     │               ╱
 0.9 │          ╱───╱
     │         ╱
 0.8 │      ╱──╱
     │     ╱
 0.7 │  ╱──╱
     │ ╱
 0.6 │╱─────┬─────┬─────┬─────┬─────
     │ Loop1│Loop2│Loop3│Loop4│Loop5
     └─────────────────────────────────
```

---

## Integração com Orquestrador

### Coleta Periódica
```python
@celery.task(name="monitor.collect_metrics")
def collect_metrics_task():
    """Coleta métricas periodicamente"""
    collector = MetricsCollector()

    # Coleta métricas de filas
    collector.collect_queue_metrics()

    # Coleta métricas de progresso de todos os projetos
    for project in ProjectStore.get_all():
        collector.collect_progress_metrics(project.name)
        collector.collect_quality_metrics(project.name)
```

### Monitoramento de Alertas
```python
@celery.task(name="monitor.check_alerts")
def check_alerts_task():
    """Verifica condições de alerta"""
    alert_manager = AlertManager()

    # Monitora filas
    alert_manager.monitor_queues()

    # Monitora qualidade de todos os projetos
    for project in ProjectStore.get_all():
        alert_manager.monitor_quality(project.name)
```

---

## Comandos CLI

```bash
# Ver status atual
monitor status

# Ver métricas de filas
monitor queues

# Ver progresso do projeto
monitor progress --project alan_nicolas

# Ver qualidade do projeto
monitor quality --project alan_nicolas

# Configurar alertas
monitor alerts configure --channel telegram

# Testar alertas
monitor alerts test --type critical
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Coleta de métricas básica
- [ ] Alertas por Telegram
- [ ] Dashboard 1 (Status Geral)

### v0.5
- [ ] Alertas por email e Slack
- [ ] Dashboard 2 (Filas)
- [ ] Dashboard 3 (Qualidade)
- [ ] Histórico de métricas

### v1.0
- [ ] Grafana completo
- [ ] Alertas customizáveis
- [ ] Níveis de urgência
- [ ] Integração completa com Prometheus

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 9*
