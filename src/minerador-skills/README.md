# Minerador de Skills

**Versão:** 1.0
**Data:** 2026-01-31

---

## Visão Geral

Minerador de Skills extraí patterns reutilizáveis de conversas, brainstorms e dados minerados.

### Módulos

- **miner.py** — SkillMiner (classe principal)
- **extractor.py** — SkillExtractor (extrai skills com OpenAI)
- **search.py** — SkillSearch (RAG para buscar skills)
- **suggester.py** — SkillSuggester (sugere skills para novos projetos)

---

## Funcionalidades

### Core
- ✅ Extrai skills de conversas
- ✅ Extrai skills de brainstorms
- ✅ Extrai skills de dados minerados
- ✅ Salva skills em banco (SQLite)
- ✅ Cria embeddings para skills (ChromaDB)
- ✅ Busca skills relevantes
- ✅ Sugere skills para novos projetos

### Tipos de Skills
- **processo** — Como estruturar brainstorm, criar PRDs, etc.
- **tecnico** — Patterns de código, arquiteturas, integrações
- **conhecimento** — Frameworks cognitivos, mentalidades, conceitos
- **negocio** — Estratégias de pricing, táticas de marketing, workflows

---

## Uso Básico

```python
from minerador_skills.miner import SkillMiner

# Inicia minerador
miner = SkillMiner()

# Minera skills de conversa
skills = miner.mine_from_conversation("session_123")

# Busca skills
skills = miner.search_skills("brainstorm estrutural")

# Sugere skills
skills = miner.suggest_skills("Criar ecossistema de mentes")
```

---

## CLI

```bash
# Minerar skills
minerador-skills mine --conversation session_123
minerador-skills mine --brainstorm brainstorm_456
minerador-skills mine --mined-data project_001

# Buscar skills
minerador-skills search --query "brainstorm estrutural"

# Sugerir skills
minerador-skills suggest --project "Criar ecossistema"

# Listar skills
minerador-skills list --type processo

# Ver skill específico
minerador-skills get --id skill_001
```

---

## Roadmap

### v0.1 (MVP) — EM PROGRESSO
- [x] Estrutura de diretórios
- [x] SkillMiner (classe principal)
- [ ] SkillExtractor (OpenAI integration)
- [ ] SkillSearch (ChromaDB integration)
- [ ] SkillSuggester
- [ ] Banco skills.db (SQLite)

### v0.5
- [ ] Integração com Sessions (auto-mineração)
- [ ] Integração com Orquestrador (mineração de brainstorms)
- [ ] CLI completa
- [ ] Testes

### v1.0
- [ ] Dashboard de skills
- [ ] Skills versionados
- [ ] A/B testing de skills
- [ ] Auto-tuning de extração

---

## Critérios de Sucesso

- [ ] Minera skills de conversas corretamente
- [ ] Minera skills de brainstorms corretamente
- [ ] Minera skills de dados minerados corretamente
- [ ] Busca de skills funciona (RAG)
- [ ] Sugestão de skills funciona
- [ ] Skills salvos em SQLite + ChromaDB
- [ ] Auto-mineração após conversas
- [ ] Unit tests coverage > 80%

---

**Última atualização:** 2026-01-31
**Status:** Em progresso
