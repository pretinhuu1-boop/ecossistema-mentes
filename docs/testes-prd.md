# TESTES — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Média (GAP 10)

---

## Problema

**Hoje:**
- Roadmap fala em "Testes"
- **Mas NENHUM plano de WHAT testar**

**Precisamos de:**
- Testes de unidade (cada módulo)
- Testes de integração (módulos entre si)
- Testes de qualidade (extração correta?)
- Testes de carga (RAG escala?)

---

## Stack Técnica

### Motor (Python)
- **pytest** — Framework de testes
- **pytest-cov** — Cobertura de código
- **pytest-asyncio** — Testes assíncronos
- **locust** — Testes de carga

### Integração
- **Todos os módulos** — São testados
- **CI/CD** — Roda testes automaticamente

---

## Funcionalidades

### Testes de Unidade
- [ ] Testar cada função isoladamente
- [ ] Mock de dependências externas
- [ ] Cobertura > 80%

### Testes de Integração
- [ ] Testar módulos entre si
- [ ] Rastreador → Minerador → Construtor
- [ ] Orquestrador + todos os módulos

### Testes de Qualidade
- [ ] Extração de artefatos correta?
- [ ] Mentes coerentes?
- [ ] Decisões fazem sentido?

### Testes de Carga
- [ ] RAG escala com 1M embeddings?
- [ ] Filas aguentam 1K tasks/min?
- [ ] Sistema suporta 1000 queries/s?

---

## Estrutura de Testes

```
tests/
├── conftest.py                    ← Configuração pytest
├── fixtures/                      ← Fixtures compartilhadas
│   ├── artifacts.py
│   ├── minds.py
│   └── events.py
│
├── unit/                          ← Testes de unidade
│   ├── test_rastreador/
│   │   ├── test_crawler.py
│   │   ├── test_etl.py
│   │   └── test_source_intelligence.py
│   ├── test_minerador/
│   │   ├── test_extractor.py
│   │   ├── test_validator.py
│   │   └── test_confidence.py
│   ├── test_orquestrador/
│   │   ├── test_events.py
│   │   ├── test_publisher.py
│   │   └── test_tasks.py
│   ├── test_rag/
│   │   ├── test_ingestor.py
│   │   ├── test_retriever.py
│   │   └── test_embedding_manager.py
│   ├── test_construtor/
│   │   ├── test_mind_builder.py
│   │   ├── test_mind_signature.py
│   │   └── test_hybridizer.py
│   └── test_squads/
│       ├── test_decision_framework.py
│       └── test_squad_generator.py
│
├── integration/                   ← Testes de integração
│   ├── test_rastreador_minerador_flow.py
│   ├── test_minerador_construtor_flow.py
│   ├── test_orquestrator_integration.py
│   └── test_rag_integration.py
│
├── quality/                       ← Testes de qualidade
│   ├── test_artifact_extraction_accuracy.py
│   ├── test_mind_coherence.py
│   └── test_decision_quality.py
│
└── load/                         ← Testes de carga
    ├── test_rag_scalability.py
    ├── test_queue_capacity.py
    └── test_system_throughput.py
```

---

## Exemplo: Testes de Unidade

### test_extractor.py
```python
"""
Testes de unidade do Minerador Extractor
"""

import pytest
from src.minerador.extractor import ArtifactExtractor

class TestArtifactExtractor:
    def test_extract_mental_model(self):
        """Testa extração de modelo mental"""
        extractor = ArtifactExtractor()

        text = "Primeiros princípios: quebrar um problema nos seus elementos fundamentais"

        result = extractor.extract(text)

        assert result["type"] == "mental_model"
        assert "Primeiros Princípios" in result["title"]
        assert result["confidence"] > 0

    def test_extract_heuristic(self):
        """Testa extração de heurística"""
        extractor = ArtifactExtractor()

        text = "Regra 80/20: 20% do esforço gera 80% do resultado"

        result = extractor.extract(text)

        assert result["type"] == "heuristic"
        assert "80/20" in result["title"]
        assert result["confidence"] > 0

    def test_extract_with_low_confidence(self):
        """Testa extração com baixa confiança"""
        extractor = ArtifactExtractor()

        text = "Texto vago e sem padrão claro"

        result = extractor.extract(text)

        assert result["confidence"] < 0.5
        assert result["type"] == "unknown"

    @pytest.mark.parametrize("text,expected_type", [
        ("Primeiros princípios", "mental_model"),
        ("Regra 80/20", "heuristic"),
        ("Design Thinking", "framework"),
    ])
    def test_extract_various_types(self, text, expected_type):
        """Testa extração de vários tipos"""
        extractor = ArtifactExtractor()

        result = extractor.extract(text)

        assert result["type"] == expected_type
```

---

## Exemplo: Testes de Integração

### test_rastreador_minerador_flow.py
```python
"""
Testes de integração: Rastreador → Minerador
"""

import pytest
from src.orquestrador.flow import start_collection
from src.orquestrador.events import EventType, subscriber
from src.minerador.extractor import ArtifactExtractor

class TestRastreadorMineradorFlow:
    @pytest.fixture
    def test_project(self):
        return {
            "name": "test_project",
            "sources": [
                {"id": "source_001", "type": "text", "content": "Primeiros princípios..."}
            ]
        }

    def test_flow_complete(self, test_project):
        """Testa fluxo completo"""
        # Eventos coletados
        collected = []
        extracted = []

        @subscriber(EventType.SOURCE_COLLECTED)
        def on_collected(event):
            collected.append(event)

        @subscriber(EventType.ARTIFACT_EXTRACTED)
        def on_extracted(event):
            extracted.append(event)

        # Inicia coleta
        start_collection(test_project["name"])

        # Aguarda um pouco (ou usa asyncio)
        import time
        time.sleep(2)

        # Verifica
        assert len(collected) == len(test_project["sources"])
        assert len(extracted) > 0

        # Verifica conteúdo
        for extraction in extracted:
            assert "artifact_id" in extraction
            assert "source_id" in extraction
```

---

## Exemplo: Testes de Qualidade

### test_artifact_extraction_accuracy.py
```python
"""
Testes de qualidade: Acerto da extração de artefatos
"""

import pytest
from src.minerador.extractor import ArtifactExtractor

class TestArtifactExtractionAccuracy:
    def test_accuracy_on_known_artifacts(self):
        """Testa acerto em artefatos conhecidos"""
        extractor = ArtifactExtractor()

        # Dataset de teste
        known_artifacts = [
            {
                "text": "Primeiros princípios: quebrar problemas em átomos",
                "expected_type": "mental_model",
                "expected_title": "Primeiros Princípios"
            },
            {
                "text": "Pensamento sistêmico: tudo está conectado",
                "expected_type": "mental_model",
                "expected_title": "Pensamento Sistêmico"
            },
            {
                "text": "Otimização prematura é raiz de todo mal",
                "expected_type": "heuristic",
                "expected_title": "Otimização Prematura"
            }
        ]

        correct = 0
        for known in known_artifacts:
            result = extractor.extract(known["text"])

            if (result["type"] == known["expected_type"] and
                known["expected_title"] in result["title"]):
                correct += 1

        accuracy = correct / len(known_artifacts)
        assert accuracy > 0.8  # 80% de acerto mínimo
```

---

## Exemplo: Testes de Carga

### test_rag_scalability.py
```python
"""
Testes de carga: Escalabilidade do RAG
"""

import pytest
from locust import HttpUser, task, between
from src.rag.retriever import DynamicRetriever

class RAGScalabilityUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.retriever = DynamicRetriever()

    @task
    def search_query(self):
        """Simula queries de busca"""
        queries = [
            "modelos mentais",
            "heurísticas de decisão",
            "frameworks de estratégia",
            "ecossistemas de agentes"
        ]

        import random
        query = random.choice(queries)

        results = self.retriever.retrieve(query, top_k=10)

        assert len(results) > 0
        assert all("text" in r for r in results)
```

---

## Configuração pytest

### conftest.py
```python
"""
Configuração pytest
"""

import pytest
import os

# Fixtures globais
@pytest.fixture
def sample_artifact():
    return {
        "id": "artifact_001",
        "type": "mental_model",
        "title": "Primeiros Princípios",
        "content": "Quebrar problemas em átomos",
        "confidence": 0.94
    }

@pytest.fixture
def sample_mind():
    return {
        "id": "mind_001",
        "author": "Test Author",
        "artifacts": [],
        "signature": {},
        "quality_score": 0.85
    }

# Configuração de cobertura
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marca testes lentos"
    )
    config.addinivalue_line(
        "markers", "integration: marca testes de integração"
    )
    config.addinivalue_line(
        "markers", "load: marca testes de carga"
    )
```

---

## Comandos CLI

```bash
# Rodar todos os testes
pytest

# Rodar só testes de unidade
pytest tests/unit/

# Rodar só testes de integração
pytest tests/integration/

# Rodar só testes de qualidade
pytest tests/quality/

# Rodar só testes de carga
pytest tests/load/

# Ver cobertura de código
pytest --cov=src --cov-report=html

# Rodar testes lentos
pytest -m slow

# Rodar testes em paralelo
pytest -n auto
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Testes de unidade básicos
- [ ] Testes de integração básicos
- [ ] Configuração pytest

### v0.5
- [ ] Testes de qualidade
- [ ] Cobertura > 80%
- [ ] CI/CD integration

### v1.0
- [ ] Testes de carga completos
- [ ] Cobertura > 90%
- [ ] Testes automatizados em PRs

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 10*
