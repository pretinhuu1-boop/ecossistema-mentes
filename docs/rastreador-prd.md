# RASTREADOR — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Planejamento

---

## Objetivo

Sistema robusto auto-evolutivo para **aprender a rastrear informações e minerar ouro**.

---

## Stack Técnica

### Motor (Python)
- **Scrapy** — Scraping robusto e escalável
- **Playwright** — Sites dinâmicos/JavaScript
- **Pandas** — ETL e estruturação de dados
- **SQLite** — Estado salvo localmente

### Interface (Clawdbot Skill)
- **Node.js** — Skill padrão Clawdbot
- `exec` → chama CLI Python
- Orquestração via `sessions_spawn`

---

## Funcionalidades

### Core
- [ ] Varre fontes (sites, PDFs, APIs, vídeos, áudios)
- [ ] Limpa, estrutura e fragmenta o conteúdo
- [ ] Salva em formato padronizado (JSON + Markdown)
- [ ] Estado salvo em SQLite (não perde nada entre sessões)

### Auto-Evolução
- [ ] Aprende quais fontes valem mais a pena
- [ ] Prioriza fontes com maior "valor extraído"
- [ ] Registra métricas de qualidade por fonte

### Modularidade
- [ ] Adiciona/remove fontes sem quebrar
- [ ] Plugin system pra diferentes tipos de fonte
- [ ] Config via YAML/JSON

---

## Estrutura de Saída

```json
{
  "id": "unique_id",
  "source": {
    "type": "web|pdf|api|video|audio",
    "url": "...",
    "collected_at": "2026-01-31T06:00:00Z"
  },
  "content": {
    "raw": "...",
    "cleaned": "...",
    "fragments": [
      {
        "id": "frag_001",
        "text": "...",
        "metadata": {...}
      }
    ]
  },
  "metadata": {
    "quality_score": 0.85,
    "word_count": 1234,
    "language": "pt-BR"
  }
}
```

---

## Comandos CLI

```bash
# Adicionar fonte
rastreador add --type web --url "https://exemplo.com"

# Executar coleta
rastreador run --source "exemplo.com"

# Listar fontes
rastreador list

# Ver status
rastreador status

# Exportar dados
rastreador export --format json --output ./data/
```

---

## Integração Clawdbot

### Skill: `rastreador`
```bash
# Adicionar fonte
!rastreador add https://exemplo.com

# Executar coleta
!rastreador run exemplo.com

# Status
!rastreador status
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Scraping básico de sites estáticos
- [ ] Limpeza e estruturação simples
- [ ] Export JSON

### v0.5
- [ ] Playwright pra sites dinâmicos
- [ ] PDF parsing
- [ ] Sistema de métricas

### v1.0
- [ ] Auto-evolução (aprende fontes valiosas)
- [ ] Plugin system
- [ ] Integração completa com Minerador

---

*Documento v1.0 — Criado em 2026-01-31*
