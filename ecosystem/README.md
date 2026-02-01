# ECOSSISTEMA DE MENTES — README

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Planejamento
**Autores:** Nelson Neto + Nexor

---

## 🎯 O Que É

Sistema robusto auto-evolutivo para:
1. **Rastrear informações** de múltiplas fontes
2. **Minerar artefatos cognitivos** (modelos mentais, heurísticas, frameworks)
3. **Criar Biblioteca de Mentes** reutilizáveis
4. **Gerar Ecossistemas de IA** que operam sozinhos

---

## 🧠 Conceito Central

> "Não é um chatbot. É uma infraestrutura cognitiva modular."

Baseado no framework do **Alan Nicolas** sobre ecossistemas de agentes, evoluído com:
- **Biblioteca de Mentes** — Capturar mentes completas e reutilizá-las
- **Extrator de Processos** — Metodologias e workflows executáveis
- **RAG (Retrieval-Augmented Generation)** — Economia de tokens
- **Estado Persistente** — Continuidade total, independente de contextos/tokens
- **Loop de Qualidade** — Evolui até atingir qualidade enterprise

---

## 🏗️ Arquitetura

### **4 Pilares:**

1. **RASTREADOR** (Data Squad)
   - Ingestão multi-fonte (vídeos, áudios, textos, APIs)
   - ETL cognitivo (limpeza, estruturação, fragmentação)
   - Source Intelligence (aprende fontes valiosas)
   - Cobertura exaustiva (não deixa nada pra trás)

2. **MINERADOR** (Cognition Squad)
   - Extração de artefatos cognitivos
   - Contexto de autor (biografia, evolução)
   - Validação de consistência
   - Confidence scores

3. **CONSTRUTOR DE MENTES**
   - Agrega artefatos em "pacotes mente"
   - Permite combinação de mentes (hibridização)
   - Cria ecossistemas configuráveis

4. **RAG + ESTADO**
   - RAG: Economia de 99.9% de tokens
   - Estado: Continuidade total entre sessões
   - Vector Store: ChromaDB
   - Embeddings: OpenAI text-embedding-3-small

### **Loop de Qualidade:**
```
RASTREADOR → MINERADOR → AVALIAÇÃO → ATINGIU?
                           ↓            ↓
                       MELHORAR ←──── NÃO
                           ↓
                     (LOOP)
                           ↓
                         DONE ←──── SIM
```

---

## 📁 Estrutura de Diretórios

```
ECOSSISTEMA-MENTES/
├── README.md                      ← Este arquivo
├── PROJECT.md                     ← Visão geral do projeto
│
├── docs/                          ← Documentação
│   ├── arquitetura.md             ← Arquitetura detalhada
│   ├── rastreador-prd.md          ← PRD do Rastreador
│   ├── minerador-prd.md           ← PRD do Minerador
│   ├── construtor-mentes-prd.md   ← PRD do Construtor de Mentes
│   ├── rag.md                     ← Documentação RAG
│   ├── estado.md                  ← Documentação Estado Persistente
│   ├── loop-qualidade.md          ← Documentação Loop de Qualidade
│   └── api-reference.md           ← Referência de API
│
├── src/                           ← Código fonte
│   ├── rastreador/                ← Módulo Rastreador
│   │   ├── __init__.py
│   │   ├── crawler.py             ← Scraping (Scrapy/Playwright)
│   │   ├── etl.py                 ← ETL cognitivo (Pandas)
│   │   ├── source_intelligence.py ← Inteligência de fontes
│   │   ├── dedup.py               ← Deduplicação
│   │   └── metadata.py            ← Metadados
│   │
│   ├── minerador/                 ← Módulo Minerador
│   │   ├── __init__.py
│   │   ├── extractor.py           ← Extração de artefatos
│   │   ├── author_context.py      ← Contexto de autor
│   │   ├── validator.py           ← Validação de consistência
│   │   ├── confidence.py          ← Confidence scores
│   │   └── relationships.py       ← Relacionamentos
│   │
│   ├── construtor-mentes/         ← Módulo Construtor de Mentes
│   │   ├── __init__.py
│   │   ├── mind_builder.py       ← Construtor de mentes
│   │   ├── hybridizer.py         ← Hibridização de mentes
│   │   ├── mind_validator.py     ← Validação de mentes
│   │   └── squad_generator.py    ← Geração de squads
│   │
│   ├── rag/                       ← Módulo RAG
│   │   ├── __init__.py
│   │   ├── ingestor.py            ← Ingestão + Embeddings
│   │   ├── retriever.py           ← Busca semântica
│   │   └── generator.py           ← Augmented Generation
│   │
│   └── estado/                    ← Módulo Estado Persistente
│       ├── __init__.py
│       ├── state_manager.py      ← Gerenciador de estado
│       ├── loop_tracker.py       ← Tracker de loops
│       └── metrics.py             ← Métricas de qualidade
│
├── data/                          ← Dados e estado
│   └── alan_nicolas/              ← Projeto Alan Nicolas
│       ├── estado/                ← Estado salvo
│       │   ├── estado.json        ← Estado atual
│       │   └── historico_loops.json ← Histórico
│       ├── fontes/                ← Fontes coletadas
│       │   ├── mapeamento.json    ← Mapeamento completo
│       │   └── coletadas/         ← Conteúdo extraído
│       ├── artefatos/             ← Artefatos cognitivos
│       │   ├── extraidos.json     ← Todos os artefatos
│       │   ├── validados.json     ← Artefatos validados
│       │   └── refinados.json     ← Artefatos refinados
│       ├── metricas/              ← Métricas de loops
│       │   ├── loop_1.json
│       │   ├── loop_2.json
│       │   └── loop_3.json
│       └── vector_store/          ← ChromaDB
│           └── chroma.db         ← Banco vetorial
│
├── scripts/                       ← Scripts utilitários
│   ├── setup.py                   ← Setup inicial
│   ├── install.sh                 ← Instala dependências
│   ├── run_loop.sh                ← Executa loop de qualidade
│   └── backup.sh                  ← Backup de dados
│
├── tests/                         ← Testes
│   ├── test_rastreador.py
│   ├── test_minerador.py
│   ├── test_rag.py
│   └── test_loop.py
│
└── logs/                          ← Logs
    ├── rastreador.log
    ├── minerador.log
    ├── rag.log
    └── loop.log
```

---

## 🚀 Como Começar

### **1. Setup inicial**
```bash
cd /Users/belissima/clawd/ECOSSISTEMA-MENTES
./scripts/setup.py
./scripts/install.sh
```

### **2. Configurar projeto**
```bash
# Criar configuração do projeto (ex: Alan Nicolas)
python src/setup.py create_project --name alan_nicolas --author "Alan Nicolas"
```

### **3. Executar loop de qualidade**
```bash
# Executa loop até atingir qualidade enterprise
./scripts/run_loop.sh alan_nicolas enterprise
```

### **4. Consultar estado**
```bash
# Ver onde o loop parou
python src/estado/state_manager.py status alan_nicolas
```

---

## 📊 Stack Técnica

| Componente | Stack |
|-------------|-------|
| **Rastreador** | Python, Scrapy, Playwright, Pandas, SQLite |
| **Minerador** | Python, LangChain, OpenAI API, Pandas |
| **RAG** | Python, ChromaDB, OpenAI text-embedding-3-small |
| **Estado** | Python, JSON, SQLite |
| **Interface Clawdbot** | Node.js, exec, sessions_spawn |

---

## 🎯 Roadmap

### **Fase 1 — Fundação (MVP)**
- [x] Estrutura de diretórios criada
- [ ] Documentação base (PRDs, arquitetura)
- [ ] Rastreador básico (scraping estático)
- [ ] Minerador básico (extração LLM)
- [ ] Estado persistente

### **Fase 2 — RAG + Loop**
- [ ] RAG implementado
- [ ] Loop de qualidade
- [ ] Métricas definidas
- [ ] Thresholds configuráveis

### **Fase 3 — Construtor de Mentes**
- [ ] Construtor de mentes
- [ ] Hibridização
- [ ] Geração de squads

### **Fase 4 — Produção**
- [ ] Testes completos
- [ ] Documentação final
- [ ] Integração Clawdbot
- [ ] Deploy

---

## 🤝 Contribuição

Este é um projeto estratégico. Todas as mudanças devem ser documentadas.

### **Workflow:**
1. Criar branch feature/nome-da-feature
2. Implementar mudança
3. Atualizar documentação
4. Testar
5. Pull request

---

## 📞 Suporte

- **Projeto principal:** ECOSSISTEMA-MENTES/
- **Documentos conceituais:** memory/foundation/
- **Contato:** Nelson Neto + Nexor

---

*Este é o projeto mais poderoso que já construímos. Vamos fazer algo histórico.*
