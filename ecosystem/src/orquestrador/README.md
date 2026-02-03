# src/orquestrador/README.md

**Módulo:** Orquestrador Central
**Versão:** 1.0
**Data:** 2026-01-31

---

## 🎯 Propósito

Coordenar **todos os módulos** do ecossistema em um fluxo unificado.

---

## 📁 Estrutura

```
src/orquestrador/
├── __init__.py
├── config.py                    ← Configuração (Celery, Redis)
├── events.py                     ← Definição de eventos
├── publisher.py                  ← Publica eventos
├── subscriber.py                 ← Consome eventos
├── tasks/                       ← Tasks Celery
│   ├── __init__.py
│   ├── rastreador_tasks.py       ← Tasks do Rastreador
│   ├── minerador_tasks.py        ← Tasks do Minerador
│   └── construtor_tasks.py       ← Tasks do Construtor de Mentes
├── queues.py                     ← Gerenciamento de filas
├── monitor.py                    ← Monitoramento
└── flow.py                       ← Workflow de integração
```

---

## 🚀 Como Funciona

### 1. Eventos
```python
# Define eventos
class Events(Enum):
    SOURCE_COLLECTED = "source.collected"
    SOURCE_FAILED = "source.failed"
    ARTIFACT_EXTRACTED = "artifact.extracted"
    ARTIFACT_FAILED = "artifact.failed"
    MIND_BUILT = "mind.built"
    MIND_FAILED = "mind.failed"
    QUALITY_EVALUATED = "quality.evaluated"
    LOOP_COMPLETED = "loop.completed"
```

### 2. Publicar Eventos
```python
# Rastreador completa coleta
EventPublisher.publish(Events.SOURCE_COLLECTED, {
    "source_id": "source_001",
    "content": {...}
})
```

### 3. Consumir Eventos
```python
# Minerador consome fonte coletada
@subscriber(Events.SOURCE_COLLECTED)
def on_source_collected(event_data):
    source_id = event_data["source_id"]
    content = event_data["content"]
    # Extrai artefatos...
```

---

## 📝 Tasks

### Rastreador Tasks
```python
@celery.task(name="rastreador.collect")
def collect_source(source_id, priority="normal"):
    """Coleta fonte"""
    # Coleta
    content = Rastreador.collect(source_id)

    # Publica evento
    EventPublisher.publish(Events.SOURCE_COLLECTED, {
        "source_id": source_id,
        "content": content
    })
```

### Minerador Tasks
```python
@celery.task(name="minerador.extract")
def extract_artifacts(source_id):
    """Extrai artefatos"""
    content = ContentStore.get(source_id)
    artifacts = Minerador.extract(content)

    # Publica eventos
    for artifact in artifacts:
        EventPublisher.publish(Events.ARTIFACT_EXTRACTED, {
            "artifact_id": artifact.id,
            "source_id": source_id,
            "artifact": artifact
        })
```

---

## 🔧 Configuração

### Celery + Redis
```python
# config.py
from celery import Celery

app = Celery('ecossistema')
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
)

# Filas de prioridade
app.conf.task_queues = (
    Queue('high', routing_key='high'),
    Queue('normal', routing_key='normal'),
    Queue('low', routing_key='low'),
)
```

---

*Documento v1.0*
