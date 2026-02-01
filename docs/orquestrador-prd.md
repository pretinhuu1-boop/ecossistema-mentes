# ORQUESTRADOR — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 1)

---

## Objetivo

Coordenar **todos os módulos** do ecossistema (Rastreador → Minerador → Construtor de Mentes) em um fluxo unificado, com eventos, filas e prioridades.

---

## Stack Técnica

### Motor (Python)
- **Celery** — Distributed task queue (filas e workers)
- **Redis** — Message broker e cache
- **SQLite** — Estado salvo localmente

### Integração
- **Rastreador** → Publica evento `source.collected`
- **Minerador** → Consome evento `source.collected`, publica `artifact.extracted`
- **Construtor de Mentes** → Consome evento `artifact.extracted`, publica `mind.built`
- **Estado** → Consome todos eventos, atualiza estado

---

## Funcionalidades

### Core
- [ ] Orquestra fluxo Rastreador → Minerador → Construtor de Mentes
- [ ] Gerencia filas de processamento (prioridades)
- [ ] Dispara eventos entre módulos
- [ ] Coordena múltiplos workers em paralelo

### Filas
- [ ] Fila de alta prioridade (fontes canônicas)
- [ ] Fila normal (fontes regulares)
- [ ] Fila de baixa prioridade (fontes exploratórias)

### Eventos
- [ ] `source.collected` — Fonte coletada pelo Rastreador
- [ ] `source.failed` — Falha na coleta
- [ ] `artifact.extracted` — Artefato extraído pelo Minerador
- [ ] `artifact.failed` — Falha na extração
- [ ] `mind.built` — Mente construída
- [ ] `mind.failed` — Falha na construção
- [ ] `quality.evaluated` — Qualidade avaliada
- [ ] `loop.completed` — Loop completado

### Monitoramento
- [ ] Status de filas (quantos tasks, quantos workers)
- [ ] Progresso do fluxo (onde tá cada fonte)
- [ ] Taxa de sucesso/falha por módulo
- [ ] Tempo de processamento

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                  ORQUESTRADOR CENTRAL                   │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ CELERY      │  │ REDIS       │  │ WORKERS     │    │
│  │ (Queue)     │  │ (Broker)    │  │ (Execução)  │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │            │
└─────────┼────────────────┼────────────────┼────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────┐
│                  FLUXO DE EVENTOS                         │
│                                                          │
│  1. Rastreador → [fila: alta] → source.collected       │
│        ↓                                                 │
│  2. Minerador consome → artifact.extracted             │
│        ↓                                                 │
│  3. Construtor consome → mind.built                     │
│        ↓                                                 │
│  4. Estado consome tudo → atualiza estado               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Estrutura de Eventos

### Evento: `source.collected`
```json
{
  "event": "source.collected",
  "timestamp": "2026-01-31T07:30:00Z",
  "data": {
    "source_id": "source_001",
    "type": "video",
    "url": "https://youtube.com/...",
    "collected_at": "2026-01-31T07:30:00Z",
    "priority": "high",
    "metadata": {
      "title": "Alan Nicolas - Ecossistema de Agentes",
      "duration": 1800,
      "language": "pt-BR"
    }
  }
}
```

### Evento: `artifact.extracted`
```json
{
  "event": "artifact.extracted",
  "timestamp": "2026-01-31T07:31:00Z",
  "data": {
    "artifact_id": "artifact_001",
    "source_id": "source_001",
    "type": "mental_model",
    "title": "Primeiros Princípios",
    "confidence": 0.94,
    "extracted_at": "2026-01-31T07:31:00Z"
  }
}
```

### Evento: `mind.built`
```json
{
  "event": "mind.built",
  "timestamp": "2026-01-31T07:35:00Z",
  "data": {
    "mind_id": "mind_alan_nicolas_v1",
    "author": "Alan Nicolas",
    "version": 1,
    "artifacts_count": 350,
    "built_at": "2026-01-31T07:35:00Z",
    "signature": {
      "voice_patterns": [...],
      "thinking_patterns": [...],
      "biases": [...]
    }
  }
}
```

---

## Filas de Prioridade

### Fila Alta (High Priority)
```python
QUEUE_HIGH = [
    "source_collected_canonical",
    "artifact_extracted_high_confidence"
]
```
- Fontes canônicas (livros, vídeos principais do autor)
- Artefatos com alta confiança
- Urgent requests

### Fila Normal (Normal Priority)
```python
QUEUE_NORMAL = [
    "source_collected_regular",
    "artifact_extracted_normal"
]
```
- Fontes regulares (artigos, podcasts)
- Artefatos com confiança normal

### Fila Baixa (Low Priority)
```python
QUEUE_LOW = [
    "source_collected_exploratory",
    "artifact_extracted_low_confidence"
]
```
- Fontes exploratórias (buscas secundárias)
- Artefatos com baixa confiança (só processar se houver tempo)

---

## Workflow de Integração

### 1. Iniciar Coleta
```python
def start_collection(project_name):
    """Inicia coleta de fontes"""
    project = load_project(project_name)

    for source in project.sources:
        # Dispara task do Rastreador
        rastreador_task.delay(
            source_id=source.id,
            queue=source.priority  # "high", "normal", "low"
        )
```

### 2. Rastreador Completa
```python
@celery.task(name="rastreador.collect")
def collect_source(source_id):
    """Coleta fonte"""
    try:
        # Coleta conteúdo
        content = Rastreador.collect(source_id)

        # Dispara evento
        EventPublisher.publish("source.collected", {
            "source_id": source_id,
            "content": content
        })

        return {"status": "success", "source_id": source_id}

    except Exception as e:
        # Dispara evento de erro
        EventPublisher.publish("source.failed", {
            "source_id": source_id,
            "error": str(e)
        })
        raise
```

### 3. Minerador Consome
```python
@celery.task(name="minerador.extract")
def extract_artifacts(source_id):
    """Extrai artefatos da fonte"""
    try:
        # Consome fonte coletada
        content = ContentStore.get(source_id)

        # Extrai artefatos
        artifacts = Minerador.extract(content)

        # Dispara evento para cada artefato
        for artifact in artifacts:
            EventPublisher.publish("artifact.extracted", {
                "artifact_id": artifact.id,
                "source_id": source_id,
                "artifact": artifact
            })

        return {"status": "success", "artifacts_count": len(artifacts)}

    except Exception as e:
        EventPublisher.publish("artifact.failed", {
            "source_id": source_id,
            "error": str(e)
        })
        raise
```

### 4. Construtor Consome
```python
@celery.task(name="construtor.build_mind")
def build_mind(author_id):
    """Constrói mente completa"""
    try:
        # Aggrega todos os artefatos do autor
        artifacts = ArtifactStore.get_by_author(author_id)

        # Constrói mente
        mind = Construtor.build(artifacts)

        # Dispara evento
        EventPublisher.publish("mind.built", {
            "mind_id": mind.id,
            "author_id": author_id,
            "mind": mind
        })

        return {"status": "success", "mind_id": mind.id}

    except Exception as e:
        EventPublisher.publish("mind.failed", {
            "author_id": author_id,
            "error": str(e)
        })
        raise
```

---

## Integração com Loop de Qualidade

### Loop Orquestrado
```python
def execute_quality_loop_orchestrated(project_name, threshold_level):
    """Executa loop de qualidade via Orquestrador"""

    # Inicia coleta
    start_collection(project_name)

    # Aguarda todos os artefatos serem extraídos
    wait_for_event("artifact.extracted", timeout=3600)

    # Avalia qualidade
    metrics = QualityEvaluator.evaluate(project_name)

    # Dispara evento
    EventPublisher.publish("quality.evaluated", {
        "project_name": project_name,
        "metrics": metrics
    })

    # Verifica threshold
    if not metrics.atingiu_threshold(threshold_level):
        # Melhora (re-inicia partes que falharam)
        improve_orchestrated(metrics)

        # Repete loop
        execute_quality_loop_orchestrated(project_name, threshold_level)
    else:
        # DONE
        EventPublisher.publish("loop.completed", {
            "project_name": project_name,
            "status": "done"
        })
```

---

## Monitoramento

### Status das Filas
```python
def get_queue_status():
    """Retorna status das filas"""
    return {
        "queue_high": {
            "pending": redis.llen("queue_high"),
            "processing": celery.active_count(queue="queue_high"),
            "completed": redis.get("queue_high_completed", 0)
        },
        "queue_normal": {
            "pending": redis.llen("queue_normal"),
            "processing": celery.active_count(queue="queue_normal"),
            "completed": redis.get("queue_normal_completed", 0)
        },
        "queue_low": {
            "pending": redis.llen("queue_low"),
            "processing": celery.active_count(queue="queue_low"),
            "completed": redis.get("queue_low_completed", 0)
        }
    }
```

### Progresso do Fluxo
```python
def get_flow_progress(project_name):
    """Retorna progresso do fluxo"""
    return {
        "sources_collected": EventStore.count("source.collected", project_name),
        "sources_failed": EventStore.count("source.failed", project_name),
        "artifacts_extracted": EventStore.count("artifact.extracted", project_name),
        "artifacts_failed": EventStore.count("artifact.failed", project_name),
        "minds_built": EventStore.count("mind.built", project_name),
        "total_sources": ProjectStore.get(project_name).sources_count,
        "progress_percent": calculate_progress(project_name)
    }
```

---

## Comandos CLI

```bash
# Iniciar Orquestrador
orchestrator start

# Iniciar coleta de projeto
orchestrator collect --project alan_nicolas

# Ver status das filas
orchestrator status --queues

# Ver progresso do projeto
orchestrator progress --project alan_nicolas

# Monitorar eventos em tempo real
orchestrator monitor

# Verificar tasks falhados
orchestrator inspect --failed

# Re-processar tasks falhados
orchestrator retry --failed
```

---

## Integração Clawdbot

### Skill: `orchestrator`
```bash
# Iniciar Orquestrador
!orchestrator start

# Coletar projeto
!orchestrator collect alan_nicolas

# Ver progresso
!orchestrator progress alan_nicolas
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Celery + Redis configurados
- [ ] Eventos básicos implementados
- [ ] Filas de prioridade
- [ ] Integração Rastreador → Minerador

### v0.5
- [ ] Integração Minerador → Construtor de Mentes
- [ ] Monitoramento de filas
- [ ] Retry automático de falhas
- [ ] Integração com Loop de Qualidade

### v1.0
- [ ] Monitoramento em tempo real (dashboards)
- [ ] Alertas (Telegram/Slack)
- [ ] Escala horizontal (múltiplos workers)
- [ ] Integração completa com Estado Persistente

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 1*
