# ORQUESTRADOR — IMPLEMENTAÇÃO BASE

**Versão:** 1.0
**Data:** 2026-01-31

---

## 📦 Dependências

```bash
pip install celery redis
```

---

## 🔧 config.py

```python
"""
Configuração do Orquestrador (Celery + Redis)
"""

from celery import Celery
from kombu import Queue

# Configuração Celery
app = Celery('ecossistema')

# Redis como broker e result backend
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

# Default routing
app.conf.task_default_queue = 'normal'
app.conf.task_default_routing_key = 'normal'
```

---

## 📡 events.py

```python
"""
Definição de eventos do sistema
"""

from enum import Enum
from typing import Dict, Any
import json
from datetime import datetime
import redis

# Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=2)


class EventType(Enum):
    """Tipos de eventos"""
    SOURCE_COLLECTED = "source.collected"
    SOURCE_FAILED = "source.failed"
    ARTIFACT_EXTRACTED = "artifact.extracted"
    ARTIFACT_FAILED = "artifact.failed"
    MIND_BUILT = "mind.built"
    MIND_FAILED = "mind.failed"
    QUALITY_EVALUATED = "quality.evaluated"
    LOOP_COMPLETED = "loop.completed"


class Event:
    """Evento do sistema"""

    def __init__(self, event_type: EventType, data: Dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dict"""
        return {
            "event": self.event_type.value,
            "timestamp": self.timestamp,
            "data": self.data
        }

    def to_json(self) -> str:
        """Converte para JSON"""
        return json.dumps(self.to_dict())


class EventPublisher:
    """Publica eventos no Redis"""

    def __init__(self, redis_client=None):
        self.redis = redis_client or redis.Redis(host='localhost', port=6379, db=2)

    def publish(self, event_type: EventType, data: Dict[str, Any]):
        """Publica evento"""
        event = Event(event_type, data)

        # Publica no canal de eventos
        channel = f"events:{event_type.value}"
        self.redis.publish(channel, event.to_json())

        # Salva no histórico (últimos 1000 eventos)
        history_key = f"events_history:{event_type.value}"
        self.redis.lpush(history_key, event.to_json())
        self.redis.ltrim(history_key, 0, 999)

        return event


class EventSubscriber:
    """Consome eventos do Redis"""

    def __init__(self, redis_client=None):
        self.redis = redis_client or redis.Redis(host='localhost', port=6379, db=2)
        self.subscriptions = {}

    def subscribe(self, event_type: EventType, callback):
        """Inscreve-se em um tipo de evento"""
        channel = f"events:{event_type.value}"

        if channel not in self.subscriptions:
            self.subscriptions[channel] = []

        self.subscriptions[channel].append(callback)

    def listen(self):
        """Escuta eventos em tempo real"""
        pubsub = self.redis.pubsub()

        # Inscreve em todos os canais
        for channel in self.subscriptions:
            pubsub.subscribe(channel)

        for message in pubsub.listen():
            if message['type'] == 'message':
                # Parse evento
                event_data = json.loads(message['data'])
                event_type = event_data['event']
                channel = f"events:{event_type}"

                # Executa callbacks
                if channel in self.subscriptions:
                    for callback in self.subscriptions[channel]:
                        callback(event_data)
```

---

## 🚀 publisher.py

```python
"""
Publicador de eventos (wrapper simples)
"""

from .events import EventPublisher, EventType

# Singleton
publisher = EventPublisher()

def publish(event_type: EventType, data: dict):
    """Publica evento (conveniência)"""
    return publisher.publish(event_type, data)
```

---

## 📥 subscriber.py

```python
"""
Assinante de eventos (wrapper simples)
"""

from .events import EventSubscriber, EventType

# Singleton
subscriber = EventSubscriber()

def on(event_type: EventType):
    """Decorator para inscrever em eventos"""
    def decorator(callback):
        subscriber.subscribe(event_type, callback)
        return callback
    return decorator
```

---

## 📊 monitor.py

```python
"""
Monitoramento de filas e eventos
"""

import redis
from typing import Dict, Any

class QueueMonitor:
    """Monitora filas do Celery"""

    def __init__(self, redis_client=None):
        self.redis = redis_client or redis.Redis(host='localhost', port=6379, db=2)

    def get_queue_status(self) -> Dict[str, Any]:
        """Retorna status das filas"""
        return {
            "high": {
                "pending": self.redis.llen("celery:queue:high"),
                "processing": self.redis.scard("celery:reserved:high"),
            },
            "normal": {
                "pending": self.redis.llen("celery:queue:normal"),
                "processing": self.redis.scard("celery:reserved:normal"),
            },
            "low": {
                "pending": self.redis.llen("celery:queue:low"),
                "processing": self.redis.scard("celery:reserved:low"),
            }
        }

    def get_event_count(self, event_type: str) -> int:
        """Retorna contagem de eventos de um tipo"""
        history_key = f"events_history:{event_type}"
        return self.redis.llen(history_key)


class ProgressMonitor:
    """Monitora progresso do projeto"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.redis = redis.Redis(host='localhost', port=6379, db=2)

    def get_progress(self) -> Dict[str, Any]:
        """Retorna progresso do projeto"""
        return {
            "sources_collected": self.redis.get(f"progress:{self.project_name}:sources_collected", 0),
            "artifacts_extracted": self.redis.get(f"progress:{self.project_name}:artifacts_extracted", 0),
            "minds_built": self.redis.get(f"progress:{self.project_name}:minds_built", 0),
        }
```

---

## 🔗 flow.py

```python
"""
Workflow de integração Rastreador → Minerador → Construtor
"""

from .tasks.rastreador_tasks import collect_source
from .tasks.minerador_tasks import extract_artifacts
from .tasks.construtor_tasks import build_mind
from .events import EventType
from .monitor import ProgressMonitor

def start_collection(project_name: str):
    """Inicia coleta de projeto"""
    # Carrega projeto (TODO: implementar)
    project = load_project(project_name)

    # Dispara coleta de cada fonte
    for source in project.sources:
        collect_source.delay(
            source_id=source.id,
            queue=source.priority  # "high", "normal", "low"
        )


def load_project(project_name: str):
    """Carrega projeto (stub)"""
    # TODO: Implementar
    class Project:
        sources = []
    return Project()
```

---

*Arquivos base criados. Próximo: Implementar tasks.*
