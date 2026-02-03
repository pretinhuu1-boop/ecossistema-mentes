# RAG DINÂMICO — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 2)

---

## Problema

**Hoje:**
- RAG é estático — embeddings são criados uma vez e nunca atualizados
- Novos artefatos entram no sistema → embeddings não são atualizados
- Artefatos antigos podem ficar obsoletos → embeddings não refletem mudanças

**Precisamos de:**
- RAG Dinâmico — embeddings são atualizados automaticamente
- Versionamento de embeddings (v1, v2, v3)
- Re-embedding incremental (só atualiza o que mudou)

---

## Stack Técnica

### Motor (Python)
- **ChromaDB** — Vector store (suporta atualizações)
- **OpenAI API** — text-embedding-3-small (embeddings)
- **SQLite** — Metadados de versões

### Integração
- **Orquestrador** → Dispara evento `artifact.updated` → RAG atualiza
- **Minerador** → Consome evento → Re-embeda artefato
- **Estado** → Registra versão de embeddings

---

## Funcionalidades

### Core
- [ ] Atualiza embeddings automaticamente quando artefatos mudam
- [ ] Versiona embeddings (v1, v2, v3)
- [ ] Re-embeda incrementalmente (só o que mudou)
- [ ] Detecta embeddings obsoletos

### Versionamento
- [ ] Cada embedding tem versão
- [ ] Histórico de versões
- [ ] Rollback para versões anteriores

### Detecção de Obsolescência
- [ ] Embeddings não atualizados em X dias → Marca como obsoleto
- [ ] Score de "freshness" (0-1, 1 = muito recente)
- [ ] Prioriza embeddings recentes nas buscas

---

## Estrutura de Embedding

```json
{
  "id": "embedding_alan_nicolas_001",
  "artifact_id": "artifact_001",
  "version": 2,
  "vector": [0.1, 0.2, ...],
  "model": "text-embedding-3-small",
  "created_at": "2026-01-30T00:00:00Z",
  "updated_at": "2026-01-31T07:30:00Z",
  "freshness_score": 1.0,
  "is_obsolete": false,
  "history": [
    {
      "version": 1,
      "created_at": "2026-01-30T00:00:00Z",
      "vector": [0.1, 0.2, ...]
    }
  ]
}
```

---

## Workflow

### 1. Novo Artefato Criado
```
Minerador → artifact.extracted
↓
Orquestrador → dispara evento
↓
EmbeddingManager → create_embedding(artifact)
↓
ChromaDB → salva embedding v1
```

### 2. Artefato Atualizado
```
Minerador → artifact.updated
↓
Orquestrador → dispara evento
↓
EmbeddingManager → update_embedding(artifact)
↓
ChromaDB → atualiza embedding v1 → v2
↓
SQLite → registra histórico
```

### 3. Artefato Removido
```
Minerador → artifact.deleted
↓
Orquestrador → dispara evento
↓
EmbeddingManager → delete_embedding(artifact_id)
↓
ChromaDB → remove embedding
```

---

## Embedding Manager

```python
class EmbeddingManager:
    def __init__(self):
        self.chroma = ChromaDB()
        self.openai = OpenAI()

    def create_embedding(self, artifact):
        """Cria embedding novo"""
        vector = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=artifact.text
        )

        embedding = {
            "id": f"embedding_{artifact.id}",
            "artifact_id": artifact.id,
            "version": 1,
            "vector": vector,
            "created_at": datetime.now().isoformat(),
            "freshness_score": 1.0
        }

        self.chroma.add(embedding)
        return embedding

    def update_embedding(self, artifact):
        """Atualiza embedding existente"""
        # Busca embedding atual
        current = self.chroma.get(artifact.id)

        # Gera novo embedding
        new_vector = self.openai.embeddings.create(...)

        # Atualiza
        updated = {
            **current,
            "version": current["version"] + 1,
            "vector": new_vector,
            "updated_at": datetime.now().isoformat(),
            "freshness_score": 1.0,
            "history": current["history"] + [current]
        }

        self.chroma.update(artifact.id, updated)
        return updated

    def delete_embedding(self, artifact_id):
        """Remove embedding"""
        self.chroma.delete(artifact_id)

    def detect_obsolete(self, days_threshold=30):
        """Detecta embeddings obsoletos"""
        threshold_date = datetime.now() - timedelta(days=days_threshold)

        obsolete = self.chroma.query(
            where={"updated_at": {"$lt": threshold_date}}
        )

        # Marca como obsoleto
        for embedding in obsolete:
            self.chroma.update(embedding.id, {
                "is_obsolete": True,
                "freshness_score": 0.0
            })

        return obsolete
```

---

## Busca com Embeddings Dinâmicos

```python
class DynamicRetriever:
    def __init__(self):
        self.manager = EmbeddingManager()

    def retrieve(self, query, top_k=10, prefer_fresh=True):
        """Busca snippets relevantes"""

        # Detecta obsoletos periodicamente
        self.manager.detect_obsolete()

        # Busca embeddings
        results = self.chroma.query(
            query_vector=embed_query(query),
            n_results=top_k,
            where=None
        )

        # Se prefer_fresh=True, filtra por freshness_score
        if prefer_fresh:
            results = [
                r for r in results
                if r["freshness_score"] > 0.8
            ]

        return results
```

---

## Integração com Orquestrador

### Evento: artifact.updated
```python
@subscriber(EventType.ARTIFACT_UPDATED)
def on_artifact_updated(event_data):
    """Quando artefato é atualizado, re-embeda"""
    artifact_id = event_data["artifact_id"]
    artifact = ArtifactStore.get(artifact_id)

    # Atualiza embedding
    EmbeddingManager().update_embedding(artifact)
```

---

## Comandos CLI

```bash
# Atualizar embeddings obsoletos
rag update --obsolete

# Re-embedar todos os artefatos
rag re-embed --all

# Ver freshness dos embeddings
rag status --freshness

# Rollback para versão anterior
rag rollback --artifact artifact_001 --to-version 1
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Embedding Manager básico
- [ ] Atualização automática de embeddings
- [ ] Detecção de obsoletos

### v0.5
- [ ] Versionamento completo
- [ ] Rollback
- [ ] Freshness scoring

### v1.0
- [ ] Re-embedding incremental
- [ ] Busca com preferência por freshness
- [ ] Monitoramento de qualidade de embeddings

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 2*
