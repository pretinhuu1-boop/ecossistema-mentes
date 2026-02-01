# MINERADOR — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Planejamento

---

## Objetivo

Sistema de **extração de artefatos cognitivos** — detecta padrões de raciocínio, heurísticas e frameworks, criando blocos mentais reutilizáveis.

---

## Stack Técnica

### Motor (Python)
- **LangChain** — Orquestração com LLMs
- **OpenAI/Anthropic API** — Extração de padrões
- **ChromaDB** — Vetor store pra artefatos cognitivos
- **Pandas** — Manipulação dos blocos mentais

### Interface (Clawdbot Skill)
- **Node.js** — Skill padrão Clawdbot
- `exec` → chama CLI Python
- Orquestração via `sessions_spawn`

---

## Funcionalidades

### Core
- [ ] Lê conteúdo processado pelo Rastreador
- [ ] Detecta padrões de raciocínio
- [ ] Detecta heurísticas
- [ ] Detecta frameworks de pensamento
- [ ] Cria blocos mentais reutilizáveis (artefatos cognitivos)
- [ ] Salva em ChromaDB com embeddings

### Pipeline de Extração
1. Coleta textos
2. Quebra em micro-unidades
3. Detecta padrões linguísticos
4. Agrupa por tipo de raciocínio
5. Cria "blocos mentais reutilizáveis"
6. Alimenta agentes com esses blocos

### Busca Semântica
- [ ] Busca artefatos por similaridade semântica
- [ ] Retorna blocos relevantes pro contexto
- [ ] Aprende com uso (ranking de relevância)

---

## Estrutura de Artefato Cognitivo

```json
{
  "id": "artifact_001",
  "type": "mental_model|heuristic|framework|decision_structure",
  "content": {
    "title": "Nome do Modelo/Heurística",
    "description": "Descrição concisa",
    "example": "Exemplo de aplicação",
    "source": {
      "original_text": "...",
      "source_id": "rastreador_id",
      "confidence": 0.92
    }
  },
  "tags": ["business", "strategy", "decision"],
  "created_at": "2026-01-31T06:00:00Z",
  "embedding": [...]
}
```

---

## Comandos CLI

```bash
# Extrair artefatos do conteúdo do Rastreador
minerador extract --source rastreador_data/

# Buscar artefatos por similaridade
minerador search "modelo mental pra decisões rápidas"

# Listar artefatos por tipo
minerador list --type mental_model

# Ver estatísticas
minerador stats

# Exportar artefatos
minerador export --format json --output ./artifacts/
```

---

## Integração Clawdbot

### Skill: `minerador`
```bash
# Extrair artefatos
!minerador extract

# Buscar artefatos
!minerador search "modelo mental pra decisões"

# Listar tipos
!minerador list --type heuristic

# Estatísticas
!minerador stats
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Extração básica com LLM
- [ ] Categorização simples
- [ ] Armazenamento em ChromaDB

### v0.5
- [ ] Pipeline completo de extração (6 etapas)
- [ ] Busca semântica
- [ ] Ranking por relevância

### v1.0
- [ ] Auto-aprimoramento (aprende com uso)
- [ ] Sistema de feedback (correção manual)
- [ ] Integração completa com Squads

---

## Exemplo de Uso

**Input (do Rastreador):**
```
"Primeiros princípios: quebrar um problema nos seus elementos fundamentais
e reconstruir a solução a partir deles."
```

**Output (Artefato Cognitivo):**
```json
{
  "type": "mental_model",
  "title": "Primeiros Princípios",
  "description": "Metodologia de resolução de problemas que decompõe
  questões complexas em seus elementos mais básicos e fundamentais.",
  "example": "Em vez de perguntar 'como posso criar mais vendas?',
  pergunte 'o que são vendas na sua essência?' e reconstrua a partir daí.",
  "confidence": 0.94
}
```

---

*Documento v1.0 — Criado em 2026-01-31*
