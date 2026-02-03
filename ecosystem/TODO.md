# TODO LIST — CLONAGEM DE MENTES E ECOSSISTEMAS

**Data:** 2026-01-31
**Foco:** Começar a clonar mentes e criar ecossistemas incríveis
**Versão:** 1.0

---

## 🎯 VISÃO GERAL

### Objetivo Final
Clonar mentes de autores (Alan Nicolas, Elon Musk, Steve Jobs, etc.) e criar ecossistemas de mentes que colaboram entre si.

### Roadmap por Camadas
- **Camada 0 (Fundamentos)** → Regras, Health, Erros, Qualidade, etc.
- **Camada 1 (Infraestrutura)** → Orquestrador, Estado, RAG, Monitoramento
- **Camada 2 (Módulos de Negócio)** → Rastreador, Minerador, Construtor, Biblioteca
- **Camada 3 (Loops de Melhoria)** → Loop de Qualidade, Human Loop
- **Camada 4 (Avançado)** → Squads de IA, Hibridização Avançada
- **Camada 5 (Testes e Docs)** → Tests, Documentação

---

## 📋 PRÉ-CAMADA 0: MINERADOR DE SKILLS

### Status: ⏸️ PENDING
### Prioridade: CRÍTICA
### Dependência: Nenhuma

#### 0.0 Minerador de Skills (GAP 20)

**PRD:** `docs/minerador-skills-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **0.0.1** Criar diretório `src/skills/`
- [ ] **0.0.2** Implementar `src/skills/miner.py` (Classe SkillMiner)
- [ ] **0.0.3** Implementar extração de skills de conversas
- [ ] **0.0.4** Implementar extração de skills de brainstorms
- [ ] **0.0.5** Implementar extração de skills de dados minerados
- [ ] **0.0.6** Implementar busca de skills (RAG)
- [ ] **0.0.7** Implementar sugestão de skills
- [ ] **0.0.8** Criar banco `skills.db` (SQLite)
- [ ] **0.0.9** Configurar ChromaDB para skills
- [ ] **0.0.10** Escrever unit tests para miner
- [ ] **0.0.11** Criar CLI `skills` (comandos: suggest, search, list, get, mine)
- [ ] **0.0.12** Integrar com Sessions (auto-mineração)
- [ ] **0.0.13** Integrar com Orquestrador (mineração de brainstorms)
- [ ] **0.0.14** Testar minerador de skills localmente
- [ ] **0.0.15** Documentar Minerador de Skills (`src/skills/README.md`)

**Critérios de Sucesso:**
- [ ] Minera skills de conversas corretamente
- [ ] Minera skills de brainstorms corretamente
- [ ] Minera skills de dados minerados corretamente
- [ ] Busca de skills funciona (RAG)
- [ ] Sugestão de skills funciona
- [ ] Skills salvos em SQLite + ChromaDB
- [ ] Auto-mineração após conversas
- [ ] Unit tests coverage > 80%

---

## 📋 CAMADA 0: FUNDAMENTOS

### Status: ⏸️ PENDING
### Prioridade: CRÍTICA
### Dependência: Pré-Camada 0 100% completa

#### 0.1 RegrasEngine (GAP 19)

**PRD:** `docs/regrasengine-prd.md` ✅ (CRIADO)
**Regras:** `rules/ecossistema.yaml` + `rules/rag.yaml` (212 regras)

**Tasks:**
- [ ] **0.1.1** Criar diretório `src/regras/`
- [ ] **0.1.2** Implementar `src/regras/engine.py` (Classe RegrasEngine)
- [ ] **0.1.3** Implementar `src/regras/loader.py` (Classe RuleLoader)
- [ ] **0.1.4** Implementar `src/regras/parser.py` (Classe ConditionParser)
- [ ] **0.1.5** Implementar `src/regras/actions.py` (Classe ActionExecutor)
- [ ] **0.1.6** Implementar `src/regras/logger.py` (Classe RuleLogger)
- [ ] **0.1.7** Criar arquivo `rules/ecossistema.yaml` (100 regras)
- [ ] **0.1.8** Criar arquivo `rules/rag.yaml` (112 regras)
- [ ] **0.1.9** Escrever unit tests para `engine.py`
- [ ] **0.1.10** Escrever unit tests para `loader.py`
- [ ] **0.1.11** Escrever unit tests para `parser.py`
- [ ] **0.1.12** Escrever unit tests para `actions.py`
- [ ] **0.1.13** Escrever unit tests para `logger.py`
- [ ] **0.1.14** Criar CLI `regras` (comandos: load, evaluate, reload, history, test, stats, list)
- [ ] **0.1.15** Testar RegrasEngine localmente
- [ ] **0.1.16** Documentar RegrasEngine (`src/regras/README.md`)

**Critérios de Sucesso:**
- [ ] Todas as 212 regras carregadas corretamente
- [ ] Parser suporta todas as condições (>=, <=, >, <, ==, !=, in, not in)
- [ ] Actions executam corretamente (parar, rejeitar, retry, create_embedding, etc.)
- [ ] Histórico de decisões persiste em SQLite
- [ ] Reload em runtime funciona sem restart
- [ ] Unit tests coverage > 80%
- [ ] CLI funciona todos os comandos

---

#### 0.2 Health Checks (GAP 18)

**PRD:** `docs/health-checks-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **0.2.1** Criar diretório `src/health/`
- [ ] **0.2.2** Implementar `src/health/engine.py` (Classe HealthCheckEngine)
- [ ] **0.2.3** Implementar `src/health/checkers/base.py` (Classe BaseHealthChecker)
- [ ] **0.2.4** Implementar `src/health/checkers/redis.py` (Classe RedisHealthChecker)
- [ ] **0.2.5** Implementar `src/health/checkers/celery.py` (Classe CeleryHealthChecker)
- [ ] **0.2.6** Implementar `src/health/checkers/chroma.py` (Classe ChromaHealthChecker)
- [ ] **0.2.7** Implementar `src/health/checkers/rastreador.py` (Classe RastreadorHealthChecker)
- [ ] **0.2.8** Implementar `src/health/checkers/minerador.py` (Classe MineradorHealthChecker)
- [ ] **0.2.9** Implementar `src/health/checkers/orquestrador.py` (Classe OrquestradorHealthChecker)
- [ ] **0.2.10** Implementar `src/health/api.py` (FastAPI endpoints: /health, /health/status, /health/summary, /health/history, /health/readiness, /health/liveness)
- [ ] **0.2.11** Implementar `src/health/scheduler.py` (Classe HealthCheckScheduler)
- [ ] **0.2.12** Implementar `src/health/alerts.py` (Classe AlertManager)
- [ ] **0.2.13** Implementar `src/health/prometheus.py` (Classe HealthCheckPrometheus)
- [ ] **0.2.14** Escrever unit tests para todos os checkers
- [ ] **0.2.15** Escrever integration tests para endpoints
- [ ] **0.2.16** Criar CLI `health-check` (comandos: status, check, history, logs, alerts, metrics, report)
- [ ] **0.2.17** Configurar alertas Telegram
- [ ] **0.2.18** Testar health checks localmente
- [ ] **0.2.19** Documentar Health Checks (`src/health/README.md`)

**Critérios de Sucesso:**
- [ ] Todos os checkers implementados
- [ ] Endpoint `/health` retorna status completo (healthy/degraded/unhealthy)
- [ ] Alertas enviados corretamente para Telegram
- [ ] Health checks executam periodicamente (scheduler)
- [ ] Logs detalhados de cada check persistem
- [ ] Prometheus metrics expostas corretamente
- [ ] Unit tests coverage > 80%
- [ ] CLI funciona todos os comandos

---

#### 0.3 Critérios de Parada (GAP 11)

**PRD:** `docs/criterios-parada-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **0.3.1** Implementar `src/termination/criteria.py` (Classe TerminationCriteria)
- [ ] **0.3.2** Implementar `src/termination/state.py` (Classe TerminationState)
- [ ] **0.3.3** Criar banco `termination_state.db` (SQLite)
- [ ] **0.3.4** Integrar TerminationCriteria no Rastreador
- [ ] **0.3.5** Integrar TerminationCriteria no Minerador
- [ ] **0.3.6** Integrar TerminationCriteria no Loop de Qualidade
- [ ] **0.3.7** Escrever unit tests para criteria
- [ ] **0.3.8** Escrever unit tests para state
- [ ] **0.3.9** Criar CLI `termination` (comandos: criteria, set, history, check)
- [ ] **0.3.10** Testar critérios de parada localmente

**Critérios de Sucesso:**
- [ ] Rastreador para nos critérios certos (max_sources, min_new_sources_per_hour, etc.)
- [ ] Minerador para nos critérios certos (max_artifacts, min_confidence_mean, etc.)
- [ ] Loop para nos critérios certos (max_iterations, min_improvement, etc.)
- [ ] Histórico de paradas persiste em SQLite
- [ ] Critérios configuráveis por projeto
- [ ] Unit tests coverage > 80%

---

#### 0.4 Tratamento de Erros (GAP 12)

**PRD:** `docs/tratamento-erros-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **0.4.1** Implementar `src/errors/classifier.py` (Classe ErrorClassifier)
- [ ] **0.4.2** Implementar `src/errors/handler.py` (Classe RobustErrorHandler)
- [ ] **0.4.3** Implementar `src/errors/backoff.py` (Classe ExponentialBackoff)
- [ ] **0.4.4** Implementar `src/errors/log.py` (Classe ErrorLog)
- [ ] **0.4.5** Criar banco `error_log.db` (SQLite)
- [ ] **0.4.6** Integrar RobustErrorHandler em todos os módulos
- [ ] **0.4.7** Escrever unit tests para classifier
- [ ] **0.4.8** Escrever unit tests para handler
- [ ] **0.4.9** Escrever unit tests para backoff
- [ ] **0.4.10** Criar CLI `errors` (comandos: recent, module, type, stats)
- [ ] **0.4.11** Testar tratamento de erros localmente

**Critérios de Sucesso:**
- [ ] Erros classificados corretamente (transient, permanent, rate_limit, unknown)
- [ ] Retry com backoff exponencial funciona
- [ ] Erros permanentes não retry
- [ ] Erros rate limit esperam e retry
- [ ] Logs de erros persistem em SQLite
- [ ] Unit tests coverage > 80%

---

#### 0.5 Validação de Qualidade de Dados (GAP 13)

**PRD:** `docs/qualidade-dados-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **0.5.1** Implementar `src/quality/validator.py` (Classe DataQualityValidator)
- [ ] **0.5.2** Implementar `src/quality/readability.py` (Classe ReadabilityCalculator)
- [ ] **0.5.3** Implementar `src/quality/language.py` (Classe LanguageDetector)
- [ ] **0.5.4** Implementar `src/quality/spam.py` (Classe SpamDetector)
- [ ] **0.5.5** Integrar DataQualityValidator no Rastreador
- [ ] **0.5.6** Integrar DataQualityValidator no Minerador
- [ ] **0.5.7** Escrever unit tests para validator
- [ ] **0.5.8** Escrever unit tests para readability
- [ ] **0.5.9** Escrever unit tests para language
- [ ] **0.5.10** Escrever unit tests para spam
- [ ] **0.5.11** Criar CLI `quality` (comandos: validate, filter, stats)
- [ ] **0.5.12** Testar validação de qualidade localmente

**Critérios de Sucesso:**
- [ ] Valida conteúdo de texto (length, repetition, readability, language, spam)
- [ ] Valida vídeo (duration, resolution, audio)
- [ ] Valida áudio (duration, bitrate, language)
- [ ] Score de qualidade (0-1)
- [ ] Filtra dados de baixa qualidade (< 0.7)
- [ ] Detecta spam corretamente
- [ ] Unit tests coverage > 80%

---

#### 0.6 Detecção de Duplicados (GAP 14)

**PRD:** `docs/duplicados-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **0.6.1** Implementar `src/duplicates/detector.py` (Classe DuplicateDetector)
- [ ] **0.6.2** Implementar simhash (usando `simhash` library)
- [ ] **0.6.3** Configurar Redis para cache de hashes
- [ ] **0.6.4** Integrar DuplicateDetector no Rastreador
- [ ] **0.6.5** Integrar DuplicateDetector no Minerador
- [ ] **0.6.6** Escrever unit tests para detector
- [ ] **0.6.7** Criar CLI `duplicates` (comandos: check, clear-cache)
- [ ] **0.6.8** Testar detecção de duplicados localmente

**Critérios de Sucesso:**
- [ ] Detecta duplicados com similarity > 95%
- [ ] Cache de hashes persiste em Redis
- [ ] Não processa duplicados (economiza recursos)
- [ ] Logs de duplicados encontrados
- [ ] Unit tests coverage > 80%

---

#### 0.7 Migração de Embeddings (GAP 15)

**PRD:** `docs/migracao-embeddings-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **0.7.1** Implementar `src/embeddings/migration.py` (Classe EmbeddingMigration)
- [ ] **0.7.2** Implementar backup de embeddings
- [ ] **0.7.3** Implementar re-embeada incremental
- [ ] **0.7.4** Implementar validação pós-migração
- [ ] **0.7.5** Implementar rollback
- [ ] **0.7.6** Escrever unit tests para migration
- [ ] **0.7.7** Criar CLI `migration` (comandos: check, migrate, history, rollback, validate)
- [ ] **0.7.8** Testar migração de embeddings localmente

**Critérios de Sucesso:**
- [ ] Detecta necessidade de migração (modelo mudou)
- [ ] Faz backup antes de migrar
- [ ] Re-embeada todos os embeddings com novo modelo
- [ ] Valida após migração (checksums, modelo, count)
- [ ] Rollback funciona se falha
- [ ] Unit tests coverage > 80%

---

#### 0.8 Verificação de Integridade (GAP 16)

**PRD:** `docs/integridade-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **0.8.1** Implementar `src/integrity/checker.py` (Classe IntegrityChecker)
- [ ] **0.8.2** Criar banco `integrity_checksums.db` (SQLite)
- [ ] **0.8.3** Implementar cálculo de checksums (SHA256)
- [ ] **0.8.4** Implementar verificação de integridade
- [ ] **0.8.5** Implementar verificação periódica (cron job)
- [ ] **0.8.6** Implementar reparação de dados corrompidos
- [ ] **0.8.7** Integrar IntegrityChecker em todos os módulos
- [ ] **0.8.8** Escrever unit tests para checker
- [ ] **0.8.9** Criar CLI `integrity` (comandos: verify, verify-all, repair, stats)
- [ ] **0.8.10** Testar verificação de integridade localmente

**Critérios de Sucesso:**
- [ ] Checksums calculados corretamente (SHA256)
- [ ] Verifica integridade periodicamente (24h)
- [ ] Detecta corrupção (checksum não bate)
- [ ] Alerta quando corrompido
- [ ] Repara dados corrompidos (restore de backup)
- [ ] Unit tests coverage > 80%

---

#### 0.9 Convergência do Loop (GAP 17)

**PRD:** `docs/convergencia-loop-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **0.9.1** Implementar `src/convergence/checker.py` (Classe ConvergenceChecker)
- [ ] **0.9.2** Implementar cálculo de melhorias
- [ ] **0.9.3** Implementar detecção de oscilação
- [ ] **0.9.4** Integrar ConvergenceChecker no Loop de Qualidade
- [ ] **0.9.5** Escrever unit tests para checker
- [ ] **0.9.6** Criar CLI `convergence` (comandos: check, history, is-oscillating, reset)
- [ ] **0.9.7** Testar convergência do loop localmente

**Critérios de Sucesso:**
- [ ] Detecta convergência corretamente (melhoria < 1% em 2 iterações)
- [ ] Detecta oscilação corretamente (diferença < 5% entre iterações)
- [ ] Loop para nos critérios certos (max_iterations, etc.)
- [ ] Histórico de iterações persiste
- [ ] Unit tests coverage > 80%

---

## 📋 CAMADA 1: INFRAESTRUTURA

### Status: ⏸️ PENDING
### Prioridade: CRÍTICA
### Dependência: Camada 0 100% completa

#### 1.1 Orquestrador (GAP 1)

**PRD:** `docs/orquestrador-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **1.1.1** Configurar Celery + Redis
- [ ] **1.1.2** Criar filas de prioridade (high, normal, low)
- [ ] **1.1.3** Implementar eventos (pub/sub) - `src/orquestrador/events.py`
- [ ] **1.1.4** Implementar monitoramento de filas - `src/orquestrador/queues.py`
- [ ] **1.1.5** Implementar workflow de integração (Rastreador → Minerador → Construtor)
- [ ] **1.1.6** Escrever unit tests para eventos
- [ ] **1.1.7** Escrever integration tests para orquestração
- [ ] **1.1.8** Criar CLI `orchestrator` (comandos: start, collect, status, progress, monitor, inspect, retry)
- [ ] **1.1.9** Testar orquestrador localmente
- [ ] **1.1.10** Documentar Orquestrador (`src/orquestrador/README.md`)

**Critérios de Sucesso:**
- [ ] Celery configurado corretamente
- [ ] Filas funcionando (high, normal, low)
- [ ] Eventos publicados corretamente (source.collected, artifact.extracted, etc.)
- [ ] Monitora filas (pending, processing, completed)
- [ ] Workers processam tasks corretamente
- [ ] Unit tests coverage > 80%

---

#### 1.2 Estado Persistente (GAP 3)

**PRD:** `docs/estado-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **1.2.1** Implementar `src/estado/store.py` (Classe EstadoStore)
- [ ] **1.2.2** Implementar snapshots - `src/estado/snapshots.py`
- [ ] **1.2.3** Implementar eventos de estado - `src/estado/events.py`
- [ ] **1.2.4** Implementar replay de eventos - `src/estado/replay.py`
- [ ] **1.2.5** Escrever unit tests para store
- [ ] **1.2.6** Escrever unit tests para snapshots
- [ ] **1.2.7** Escrever unit tests para replay
- [ ] **1.2.8** Testar persistência de estado localmente
- [ ] **1.2.9** Documentar Estado (`src/estado/README.md`)

**Critérios de Sucesso:**
- [ ] Estado persiste corretamente (SQLite)
- [ ] Snapshots funcionam (criar, restaurar)
- [ ] Eventos de estado logados corretamente
- [ ] Replay de eventos funciona
- [ ] Estado consistente após replay
- [ ] Unit tests coverage > 80%

---

#### 1.3 RAG Dinâmico (GAP 2)

**PRD:** `docs/rag-dinamico-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **1.3.1** Implementar `src/rag/manager.py` (Classe EmbeddingManager)
- [ ] **1.3.2** Implementar `src/rag/retriever.py` (Classe DynamicRetriever)
- [ ] **1.3.3** Implementar versionamento de embeddings
- [ ] **1.3.4** Implementar freshness scoring
- [ ] **1.3.5** Configurar ChromaDB
- [ ] **1.3.6** Integrar com OpenAI API (text-embedding-3-small)
- [ ] **1.3.7** Escrever unit tests para manager
- [ ] **1.3.8** Escrever unit tests para retriever
- [ ] **1.3.9** Criar CLI `rag` (comandos: update, re-embed, status, rollback, validate)
- [ ] **1.3.10** Testar RAG localmente
- [ ] **1.3.11** Documentar RAG (`src/rag/README.md`)

**Critérios de Sucesso:**
- [ ] Embeddings criados automaticamente quando artefato criado
- [ ] Embeddings atualizados automaticamente quando artefato atualizado
- [ ] Versionamento funciona (v1 → v2 → v3)
- [ ] Freshness scoring funciona (decai por dia, marca obsoletos)
- [ ] Busca retorna resultados corretos
- [ ] Prioriza embeddings fresh (> 0.8)
- [ ] Unit tests coverage > 80%

---

#### 1.4 Monitoramento (GAP 4)

**PRD:** `docs/monitoramento-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **1.4.1** Implementar `src/monitoring/engine.py` (Classe MonitorEngine)
- [ ] **1.4.2** Implementar métricas (Prometheus) - `src/monitoring/metrics.py`
- [ ] **1.4.3** Implementar alertas - `src/monitoring/alerts.py`
- [ ] **1.4.4** Implementar dashboards (Grafana)
- [ ] **1.4.5** Configurar Prometheus
- [ ] **1.4.6** Configurar Grafana
- [ ] **1.4.7** Escrever unit tests para engine
- [ ] **1.4.8** Testar monitoramento localmente
- [ ] **1.4.9** Documentar Monitoramento (`src/monitoring/README.md`)

**Critérios de Sucesso:**
- [ ] Métricas coletadas corretamente (Prometheus)
- [ ] Alertas enviados corretamente (Telegram/Slack)
- [ ] Dashboards funcionam (Grafana)
- [ ] Histórico de métricas persiste
- [ ] Unit tests coverage > 80%

---

## 📋 CAMADA 2: MÓDULOS DE NEGÓCIO

### Status: ⏸️ PENDING
### Prioridade: ALTA
### Dependência: Camada 1 100% completa

#### 2.1 Rastreador (GAP 5)

**PRD:** `docs/rastreador-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **2.1.1** Implementar scraping multi-fonte (YouTube, Blogs, Livros, Podcasts) - `src/rastreador/scrapers/`
- [ ] **2.1.2** Implementar ETL cognitivo - `src/rastreador/etl.py`
- [ ] **2.1.3** Implementar Source Intelligence - `src/rastreador/intelligence.py`
- [ ] **2.1.4** Integrar com RegrasEngine
- [ ] **2.1.5** Integrar com Validação de Qualidade
- [ ] **2.1.6** Integrar com Detecção de Duplicados
- [ ] **2.1.7** Escrever unit tests para scrapers
- [ ] **2.1.8** Escrever unit tests para ETL
- [ ] **2.1.9** Escrever integration tests para rastreamento
- [ ] **2.1.10** Criar CLI `rastreador` (comandos: collect, status, sources, history)
- [ ] **2.1.11** Testar rastreador localmente
- [ ] **2.1.12** Documentar Rastreador (`src/rastreador/README.md`)

**Critérios de Sucesso:**
- [ ] Scrapeia todas as fontes (YouTube, Blogs, Livros, Podcasts)
- [ ] ETL cognitivo funciona (transcrição, extração, normalização)
- [ ] Source Intelligence funciona (prioridade, relevance, context)
- [ ] Valida qualidade antes de processar
- [ ] Detecta duplicados antes de processar
- [ ] Para nos critérios certos (TerminationCriteria)
- [ ] Unit tests coverage > 80%

---

#### 2.2 Minerador (GAP 6)

**PRD:** `docs/minerador-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **2.2.1** Implementar extração de artefatos cognitivos - `src/minerador/extractor.py`
- [ ] **2.2.2** Implementar contexto de autor - `src/minerador/context.py`
- [ ] **2.2.3** Implementar validação de consistência - `src/minerador/validator.py`
- [ ] **2.2.4** Implementar confidence scores - `src/minerador/confidence.py`
- [ ] **2.2.5** Integrar com RegrasEngine
- [ ] **2.2.6** Integrar com Validação de Qualidade
- [ ] **2.2.7** Escrever unit tests para extractor
- [ ] **2.2.8** Escrever unit tests para context
- [ ] **2.2.9** Escrever unit tests para validator
- [ ] **2.2.10** Criar CLI `minerador` (comandos: extract, artifacts, status, history)
- [ ] **2.2.11** Testar minerador localmente
- [ ] **2.2.12** Documentar Minerador (`src/minerador/README.md`)

**Critérios de Sucesso:**
- [ ] Extrai artefatos cognitivos corretamente (mental_models, frameworks, biases, etc.)
- [ ] Contexto de autor funciona (quem disse, quando, onde)
- [ ] Valida consistência (não contraditório)
- [ ] Confidence scores funcionam (0-1)
- [ ] Valida qualidade antes de processar
- [ ] Detecta duplicados antes de processar
- [ ] Para nos critérios certos (TerminationCriteria)
- [ ] Unit tests coverage > 80%

---

#### 2.3 Construtor de Mentes (GAP 7)

**PRD:** `docs/construtor-mentes-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **2.3.1** Implementar agregação de artefatos - `src/construtor/aggregator.py`
- [ ] **2.3.2** Implementar assinatura cognitiva - `src/construtor/signature.py`
- [ ] **2.3.3** Implementar validação de mente - `src/construtor/validator.py`
- [ ] **2.3.4** Implementar versionamento de mente - `src/construtor/versioning.py`
- [ ] **2.3.5** Integrar com RegrasEngine
- [ ] **2.3.6** Escrever unit tests para aggregator
- [ ] **2.3.7** Escrever unit tests para signature
- [ ] **2.3.8** Escrever unit tests para validator
- [ ] **2.3.9** Criar CLI `construtor` (comandos: build, minds, status, history)
- [ ] **2.3.10** Testar construtor localmente
- [ ] **2.3.11** Documentar Construtor (`src/construtor/README.md`)

**Critérios de Sucesso:**
- [ ] Agrega artefatos corretamente (por autor)
- [ ] Assinatura cognitiva funciona (voice_patterns, thinking_patterns, biases)
- [ ] Valida mente (coerência, coverage, consistência)
- [ ] Versionamento funciona (v1 → v2 → v3)
- [ ] Para nos critérios certos (TerminationCriteria)
- [ ] Unit tests coverage > 80%

---

#### 2.4 Biblioteca de Mentes (GAP 8)

**PRD:** `docs/hibridizacao-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **2.4.1** Implementar CRUD de mentes - `src/biblioteca/crud.py`
- [ ] **2.4.2** Implementar hibridização - `src/biblioteca/hibridizacao.py`
- [ ] **2.4.3** Implementar busca de mentes - `src/biblioteca/search.py`
- [ ] **2.4.4** Implementar exportação/importação - `src/biblioteca/export.py`
- [ ] **2.4.5** Escrever unit tests para crud
- [ ] **2.4.6** Escrever unit tests para hibridizacao
- [ ] **2.4.7** Escrever unit tests para search
- [ ] **2.4.8** Criar CLI `biblioteca` (comandos: list, get, create, update, delete, hibridize, search, export, import)
- [ ] **2.4.9** Testar biblioteca localmente
- [ ] **2.4.10** Documentar Biblioteca (`src/biblioteca/README.md`)

**Critérios de Sucesso:**
- [ ] CRUD funciona (create, read, update, delete)
- [ ] Hibridização funciona (merge de mentes)
- [ ] Busca retorna resultados corretos (por assinatura, por nome, etc.)
- [ ] Exportação/importação funciona (JSON, YAML)
- [ ] Unit tests coverage > 80%

---

## 📋 CAMADA 3: LOOPS DE MELHORIA

### Status: ⏸️ PENDING
### Prioridade: MÉDIA
### Dependência: Camada 2 100% completa

#### 3.1 Loop de Qualidade (GAP 9)

**PRD:** `docs/loop-qualidade-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **3.1.1** Implementar execução de loops - `src/qualityloop/executor.py`
- [ ] **3.1.2** Implementar avaliação de qualidade - `src/qualityloop/evaluator.py`
- [ ] **3.1.3** Implementar melhoria de gaps - `src/qualityloop/improver.py`
- [ ] **3.1.4** Integrar com RegrasEngine
- [ ] **3.1.5** Integrar com ConvergenceChecker
- [ ] **3.1.6** Escrever unit tests para executor
- [ ] **3.1.7** Escrever unit tests para evaluator
- [ ] **3.1.8** Escrever integration tests para loops
- [ ] **3.1.9** Criar CLI `qualityloop` (comandos: run, status, history, metrics)
- [ ] **3.1.10** Testar loop de qualidade localmente
- [ ] **3.1.11** Documentar Loop de Qualidade (`src/qualityloop/README.md`)

**Critérios de Sucesso:**
- [ ] Executa loops corretamente
- [ ] Avalia qualidade (coverage, confidence, consistência)
- [ ] Melhora gaps (adiciona fontes, melhora extração, etc.)
- [ ] Para quando converge (ConvergenceChecker)
- [ ] Unit tests coverage > 80%

---

#### 3.2 Human Loop (GAP 10)

**PRD:** `docs/human-loop-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **3.2.1** Implementar aprovação de artefatos - `src/humanloop/approval.py`
- [ ] **3.2.2** Implementar feedback de usuário - `src/humanloop/feedback.py`
- [ ] **3.2.3** Implementar ajuste de mentes - `src/humanloop/adjuster.py`
- [ ] **3.2.4** Integrar com CLI
- [ ] **3.2.5** Escrever unit tests para approval
- [ ] **3.2.6** Escrever unit tests para feedback
- [ ] **3.2.7** Escrever unit tests para adjuster
- [ ] **3.2.8** Testar human loop localmente
- [ ] **3.2.9** Documentar Human Loop (`src/humanloop/README.md`)

**Critérios de Sucesso:**
- [ ] Aprovação funciona (usuário aprova/rejeita artefatos)
- [ ] Feedback persiste (o que usuário disse)
- [ ] Ajustes funcionam (usuário ajusta mente)
- [ ] Unit tests coverage > 80%

---

## 📋 CAMADA 4: AVANÇADO

### Status: ⏸️ PENDING
### Prioridade: MÉDIA
### Dependência: Camada 3 100% completa

#### 4.1 Squads de IA (GAP 11 do ecossistema)

**PRD:** `docs/squads-prd.md` ✅ (CRIADO)

**Tasks:**
- [ ] **4.1.1** Implementar criação de squads - `src/squads/creator.py`
- [ ] **4.1.2** Implementar colaboração entre mentes - `src/squads/collaboration.py`
- [ ] **4.1.3** Implementar debrief de squads - `src/squads/debrief.py`
- [ ] **4.1.4** Escrever unit tests para creator
- [ ] **4.1.5** Escrever unit tests para collaboration
- [ ] **4.1.6** Escrever unit tests para debrief
- [ ] **4.1.7** Criar CLI `squads` (comandos: create, collaborate, debrief, list, status)
- [ ] **4.1.8** Testar squads localmente
- [ ] **4.1.9** Documentar Squads (`src/squads/README.md`)

**Critérios de Sucesso:**
- [ ] Squads funcionam (múltiplas mentes colaborando)
- [ ] Colaboração entre mentes funciona
- [ ] Debrief gera insights (o que funcionou, o que não)
- [ ] Unit tests coverage > 80%

---

#### 4.2 Hibridização Avançada

**Tasks:**
- [ ] **4.2.1** Implementar hibridização ponderada
- [ ] **4.2.2** Implementar hibridização contextual
- [ ] **4.2.3** Implementar hibridização dinâmica
- [ ] **4.2.4** Escrever unit tests para hibridização avançada
- [ ] **4.2.5** Testar hibridização avançada localmente

**Critérios de Sucesso:**
- [ ] Hibridização ponderada funciona (pesos configuráveis)
- [ ] Hibridização contextual funciona (baseado em contexto)
- [ ] Hibridização dinâmica funciona (adapta em runtime)
- [ ] Unit tests coverage > 80%

---

## 📋 CAMADA 5: TESTES E DOCUMENTAÇÃO

### Status: ⏸️ PENDING
### Prioridade: ALTA
### Dependência: Camada 4 100% completa

#### 5.1 Testes Automatizados

**Tasks:**
- [ ] **5.1.1** Unit tests para todos os módulos (coverage > 80%)
- [ ] **5.1.2** Integration tests para cada camada
- [ ] **5.1.3** E2E tests para workflows completos
- [ ] **5.1.4** Configurar CI/CD (GitHub Actions)
- [ ] **5.1.5** Configurar testes automáticos em cada commit

**Critérios de Sucesso:**
- [ ] Todos os módulos têm unit tests
- [ ] Integration tests funcionam
- [ ] E2E tests funcionam
- [ ] Coverage > 80%
- [ ] CI/CD executa testes automaticamente

---

#### 5.2 Documentação

**Tasks:**
- [ ] **5.2.1** README.md em cada módulo
- [ ] **5.2.2** Examples em cada módulo
- [ ] **5.2.3** API docs para todos os endpoints
- [ ] **5.2.4** Tutorial de uso completo
- [ ] **5.2.5** Troubleshooting guide

**Critérios de Sucesso:**
- [ ] Todos os módulos têm README
- [ ] Examples funcionam
- [ ] API docs completas
- [ ] Tutorial cobre tudo
- [ ] Troubleshooting útil

---

## 🚀 PROJETOS PILOTO

### Status: ⏸️ PENDING
### Dependência: Camada 5 100% completa

#### PROJETO 1: Alan Nicolas

**Tasks:**
- [ ] **P1.1** Definir fontes (YouTube, Blog, Livros)
- [ ] **P1.2** Executar Rastreador para Alan Nicolas
- [ ] **P1.3** Executar Minerador para Alan Nicolas
- [ ] **P1.4** Construir mente de Alan Nicolas
- [ ] **P1.5** Executar Loop de Qualidade
- [ ] **P1.6** Validar mente (assinaratura coerente)
- [ ] **P1.7** Testar busca RAG
- [ ] **P1.8** Documentar mente de Alan Nicolas

**Critérios de Sucesso:**
- [ ] Mente de Alan Nicolas construída
- [ ] Assinatura cognitiva coerente
- [ ] Busca RAG funciona
- [ ] Qualidade alta (coverage > 90%, confidence > 0.85)

---

#### PROJETO 2: Elon Musk

**Tasks:**
- [ ] **P2.1** Definir fontes (YouTube, Twitter, Biografias)
- [ ] **P2.2** Executar Rastreador para Elon Musk
- [ ] **P2.3** Executar Minerador para Elon Musk
- [ ] **P2.4** Construir mente de Elon Musk
- [ ] **P2.5** Executar Loop de Qualidade
- [ ] **P2.6** Validar mente (assinaratura coerente)
- [ ] **P2.7** Testar busca RAG
- [ ] **P2.8** Documentar mente de Elon Musk

**Critérios de Sucesso:**
- [ ] Mente de Elon Musk construída
- [ ] Assinatura cognitiva coerente
- [ ] Busca RAG funciona
- [ ] Qualidade alta (coverage > 90%, confidence > 0.85)

---

#### PROJETO 3: Squad Alan + Elon

**Tasks:**
- [ ] **P3.1** Criar squad Alan + Elon
- [ ] **P3.2** Executar colaboração (discussão entre mentes)
- [ ] **P3.3** Executar debrief
- [ ] **P3.4** Documentar squad

**Critérios de Sucesso:**
- [ ] Squad criado
- [ ] Colaboração entre mentes funciona
- [ ] Debrief gera insights
- [ ] Squad documentado

---

## 📊 RESUMO DE TASKS

| Camada | Tasks Total | Concluídas | Pendentes |
|--------|-------------|------------|------------|
| **Pré-0** | Minerador de Skills | 0 | ~15 |
| **0** | Fundamentos | 0 | ~200 |
| **1** | Infraestrutura | 0 | ~40 |
| **2** | Módulos de Negócio | 0 | ~50 |
| **3** | Loops de Melhoria | 0 | ~25 |
| **4** | Avançado | 0 | ~10 |
| **5** | Testes e Docs | 0 | ~10 |
| **Projetos Piloto** | 3 Projetos | 0 | ~24 |
| **TOTAL** | **~374 Tasks** | **0** | **~374** |

---

## 🎯 PRÓXIMOS PASSOS

### **HOJE:**
1. ✅ Criar TODO LIST (FEITO!)
2. ⏸️ Começar **Camada 0.1: RegrasEngine**

### **AMANHÃ:**
1. Completar **Pré-Camada 0.0: Minerador de Skills** (ou começar 0.1 RegrasEngine)
2. Continuar **Camada 0.1: RegrasEngine**
3. Começar **Camada 0.2: Health Checks**

### **PRÓXIMA SEMANA:**
1. Completar **Camada 0** (Fundamentos)
2. Começar **Camada 1** (Infraestrutura)

---

**Tio Bet, TODO LIST CRIADO!** 🥷🏾

**~359 tasks mapeadas, prontas para serem executadas!**

**Queremos começar pela Camada 0.1 (RegrasEngine)?**
