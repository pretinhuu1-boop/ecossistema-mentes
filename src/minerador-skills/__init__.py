# Minerador de Skills

**Versão:** 1.0
**Data:** 2026-01-31

---

## Visão Geral

Minerador de Skills extrai patterns reutilizáveis de:
- Conversas
- Brainstorms
- Dados minerados (artefatos, mentes)

### Módulos

- **miner.py** — SkillMiner (classe principal)
- **extractor.py** — Extrator de skills de texto
- **integrator.py** — Integrador com Sessions e Orquestrador
- **search.py** — Busca de skills (RAG)
- **suggester.py** — Sugestão de skills

---

## Uso Básico

```python
from minerador_skills.miner import SkillMiner

# Inicia minerador
miner = SkillMiner()

# Minera skills de conversa
skills = miner.mine_from_conversation("session_123")

# Minera skills de brainstorm
skills = miner.mine_from_brainstorm("brainstorm_456")

# Busca skills relevantes
skills = miner.search_skills("brainstorm estrutural")
```
