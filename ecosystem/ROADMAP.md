# ROADMAP DO ECOSSISTEMA — O QUE EXECUTAR

**Versão:** 1.0
**Data:** 2026-01-31
**Foco:** O QUE fazer, não QUANDO
**Princípio:** Qualidade sobre velocidade

---

## 🎯 PRINCÍPIOS FUNDAMENTAIS

### 1. **QUALIDADE SOBRE VELOCIDADE**
- Cada PRD deve ser implementado com perfeição
- Testes automáticos para tudo
- Refactoring constante

### 2. **REGRAS PRIMEIRO, IMPLEMENTAÇÃO DEPOIS**
- Regras em YAML/JSON antes de código
- Engine de regras funcionando
- Depois implementa módulos

### 3. **TESTABILIDADE SEMPRE**
- Cada módulo testável isoladamente
- Mocks para dependências externas
- Coverage > 80%

### 4. **OBSERVABILIDADE NATIVA**
- Logs estruturados desde o começo
- Métricas em tudo
- Health checks em cada módulo

### 5. **DOCUMENTAÇÃO VIVA**
- PRDs como fonte da verdade
- README em cada módulo
- Examples sempre atualizados

---

## 📋 ROADMAP POR CAMADAS

---

## CAMADA 0: FUNDAMENTOS

### Objetivo
Criar a fundação sólida onde tudo vai ser construído

### O que deve ser feito

#### 0.1 RegrasEngine (GAP 19)
- [ ] Implementar `RegrasEngine`
- [ ] Implementar `RuleLoader` (YAML)
- [ ] Implementar `ConditionParser`
- [ ] Implementar `ActionExecutor`
- [ ] Implementar `RuleLogger`
- [ ] Criar `rules/ecossistema.yaml` (100 regras)
- [ ] Criar `rules/rag.yaml` (112 regras)
- [ ] Testes unitários do engine
- [ ] CLI para gerenciar regras

**Critérios de qualidade:**
- Todas as 212 regras carregadas corretamente
- Parser suporta todas as condições
- Actions executam corretamente
- Histórico de decisões persiste
- Reload em runtime funciona

---

#### 0.2 Health Checks (GAP 18)
- [ ] Implementar `HealthCheckEngine`
- [ ] Implementar `RedisHealthChecker`
- [ ] Implementar `CeleryHealthChecker`
- [ ] Implementar `ChromaHealthChecker`
- [ ] Implementar `RastreadorHealthChecker`
- [ ] Implementar `MineradorHealthChecker`
- [ ] Implementar `OrquestradorHealthChecker`
- [ ] Criar endpoint `/health`
- [ ] Criar `AlertManager` (Telegram/Slack)
- [ ] Testes de health checks

**Critérios de qualidade:**
- Todos os checkers implementados
- Endpoint `/health` retorna status completo
- Alertas enviados corretamente
- Health checks executam periodicamente
- Logs detalhados de cada check

---

#### 0.3 Critérios de Parada (GAP 11)
- [ ] Implementar `TerminationCriteria`
- [ ] Implementar `TerminationState`
- [ ] Integrar no Rastreador
- [ ] Integrar no Minerador
- [ ] Integrar no Loop de Qualidade
- [ ] Testes de critérios de parada

**Critérios de qualidade:**
- Rastreador para nos critérios certos
- Minerador para nos critérios certos
- Loop para nos critérios certos
- Histórico de paradas persiste
- Critérios configuráveis por projeto

---

#### 0.4 Tratamento de Erros (GAP 12)
- [ ] Implementar `ErrorClassifier`
- [ ] Implementar `RobustErrorHandler`
- [ ] Implementar `ExponentialBackoff`
- [ ] Implementar `ErrorLog`
- [ ] Integrar em todos os módulos
- [ ] Testes de tratamento de erros

**Critérios de qualidade:**
- Erros classificados corretamente
- Retry com backoff funciona
- Erros permanentes não retry
- Logs de erros persistem
- Alertas enviados corretamente

---

#### 0.5 Validação de Qualidade de Dados (GAP 13)
- [ ] Implementar `DataQualityValidator`
- [ ] Implementar `SpamDetector`
- [ ] Implementar `ReadabilityCalculator`
- [ ] Implementar `LanguageDetector`
- [ ] Integrar no Rastreador
- [ ] Integrar no Minerador
- [ ] Testes de validação de qualidade

**Critérios de qualidade:**
- Valida conteúdo, vídeo e áudio
- Detecta spam corretamente
- Score de qualidade (0-1)
- Filtra dados de baixa qualidade
- Logs de rejeições

---

#### 0.6 Detecção de Duplicados (GAP 14)
- [ ] Implementar `DuplicateDetector`
- [ ] Implementar simhash
- [ ] Implementar cache de hashes
- [ ] Integrar no Rastreador
- [ ] Integrar no Minerador
- [ ] Testes de detecção de duplicados

**Critérios de qualidade:**
- Detecta duplicados com similarity > 95%
- Cache de hashes persiste
- Não processa duplicados
- Logs de duplicados encontrados

---

#### 0.7 Migração de Embeddings (GAP 15)
- [ ] Implementar `EmbeddingMigration`
- [ ] Implementar backup de embeddings
- [ ] Implementar re-embeada incremental
- [ ] Implementar validação pós-migração
- [ ] Implementar rollback
- [ ] Testes de migração

**Critérios de qualidade:**
- Detecta necessidade de migração
- Faz backup antes
- Re-embeada corretamente
- Valida após migração
- Rollback funciona

---

#### 0.8 Verificação de Integridade (GAP 16)
- [ ] Implementar `IntegrityChecker`
- [ ] Implementar cálculo de checksums
- [ ] Implementar verificação periódica
- [ ] Integrar em todos os módulos
- [ ] Testes de integridade

**Critérios de qualidade:**
- Checksums calculados corretamente
- Verifica integridade periodicamente
- Detecta corrupção
- Alerta quando corrompido
- Repositórios de integridade persistem

---

#### 0.9 Convergência do Loop (GAP 17)
- [ ] Implementar `ConvergenceChecker`
- [ ] Implementar detecção de oscilação
- [ ] Integrar no Loop de Qualidade
- [ ] Testes de convergência

**Critérios de qualidade:**
- Detecta convergência corretamente
- Detecta oscilação
- Loop para nos critérios certos
- Histórico de iterações persiste

---

## CAMADA 1: INFRAESTRUTURA

### Objetivo
Criar a infraestrutura onde os módulos vão rodar

### O que deve ser feito

#### 1.1 Orquestrador (GAP 1)
- [ ] Configurar Celery + Redis
- [ ] Implementar filas de prioridade
- [ ] Implementar eventos (pub/sub)
- [ ] Implementar monitoramento de filas
- [ ] CLI para gerenciar filas
- [ ] Testes de orquestração

**Critérios de qualidade:**
- Celery configurado corretamente
- Filas funcionando
- Publica eventos corretamente
- Monitora filas
- Workers processam tasks

---

#### 1.2 Estado Persistente (GAP 3)
- [ ] Implementar `EstadoStore`
- [ ] Implementar snapshots
- [ ] Implementar eventos de estado
- [ ] Implementar replay de eventos
- [ ] Testes de persistência

**Critérios de qualidade:**
- Estado persiste corretamente
- Snapshots funcionam
- Replay de eventos funciona
- Eventos logados
- Estado consistente

---

#### 1.3 RAG Dinâmico (GAP 2)
- [ ] Implementar `EmbeddingManager`
- [ ] Implementar `DynamicRetriever`
- [ ] Implementar versionamento de embeddings
- [ ] Implementar freshness scoring
- [ ] Integrar com ChromaDB
- [ ] Testes de RAG

**Critérios de qualidade:**
- Embeddings criados/atuais
- Versionamento funciona
- Freshness scoring funciona
- Busca retorna resultados corretos
- Migração de embeddings funciona

---

#### 1.4 Monitoramento (GAP 4)
- [ ] Implementar `MonitorEngine`
- [ ] Implementar métricas (Prometheus)
- [ ] Implementar alertas
- [ ] Implementar dashboards
- [ ] Testes de monitoramento

**Critérios de qualidade:**
- Métricas coletadas corretamente
- Alertas enviados corretamente
- Dashboards funcionam
- Histórico de métricas persiste

---

## CAMADA 2: MÓDULOS DE NEGÓCIO

### Objetivo
Implementar os módulos que fazem o trabalho real

### O que deve ser feito

#### 2.1 Rastreador (GAP 5)
- [ ] Implementar scraping multi-fonte
- [ ] Implementar ETL cognitivo
- [ ] Implementar Source Intelligence
- [ ] Integrar com RegrasEngine
- [ ] Integrar com Validação de Qualidade
- [ ] Integrar com Detecção de Duplicados
- [ ] Testes de rastreamento

**Critérios de qualidade:**
- Scrapeia todas as fontes
- ETL cognitivo funciona
- Source Intelligence funciona
- Valida qualidade
- Detecta duplicados
- Para nos critérios certos

---

#### 2.2 Minerador (GAP 6)
- [ ] Implementar extração de artefatos cognitivos
- [ ] Implementar contexto de autor
- [ ] Implementar validação de consistência
- [ ] Implementar confidence scores
- [ ] Integrar com RegrasEngine
- [ ] Integrar com Validação de Qualidade
- [ ] Testes de mineração

**Critérios de qualidade:**
- Extrai artefatos corretamente
- Contexto de autor funciona
- Valida consistência
- Confidence scores funcionam
- Valida qualidade
- Para nos critérios certos

---

#### 2.3 Construtor de Mentes (GAP 7)
- [ ] Implementar agregação de artefatos
- [ ] Implementar assinatura cognitiva
- [ ] Implementar validação de mente
- [ ] Implementar versionamento de mente
- [ ] Integrar com RegrasEngine
- [ ] Testes de construção

**Critérios de qualidade:**
- Agrega artefatos corretamente
- Assinatura cognitiva funciona
- Valida mente
- Versionamento funciona
- Para nos critérios certos

---

#### 2.4 Biblioteca de Mentes (GAP 8)
- [ ] Implementar CRUD de mentes
- [ ] Implementar hibridização
- [ ] Implementar busca de mentes
- [ ] Implementar exportação/importação
- [ ] Testes de biblioteca

**Critérios de qualidade:**
- CRUD funciona
- Hibridização funciona
- Busca retorna resultados
- Exportação/importação funciona

---

## CAMADA 3: LOOPS DE MELHORIA

### Objetivo
Implementar os loops que melhoram o sistema constantemente

### O que deve ser feito

#### 3.1 Loop de Qualidade (GAP 9)
- [ ] Implementar execução de loops
- [ ] Implementar avaliação de qualidade
- [ ] Implementar melhoria de gaps
- [ ] Integrar com RegrasEngine
- [ ] Integrar com ConvergenceChecker
- [ ] Testes de loops

**Critérios de qualidade:**
- Executa loops corretamente
- Avalia qualidade
- Melhora gaps
- Para quando converge

---

#### 3.2 Human Loop (GAP 10)
- [ ] Implementar aprovação de artefatos
- [ ] Implementar feedback de usuário
- [ ] Implementar ajuste de mentes
- [ ] Integrar com CLI
- [ ] Testes de human loop

**Critérios de qualidade:**
- Aprovação funciona
- Feedback persiste
- Ajustes funcionam

---

## CAMADA 4: AVANÇADO

### Objetivo
Funcionalidades avançadas que fazem o sistema poderoso

### O que deve ser feito

#### 4.1 Squads de IA (GAP 11 do ecossistema)
- [ ] Implementar criação de squads
- [ ] Implementar colaboração entre mentes
- [ ] Implementar debrief de squads
- [ ] Testes de squads

**Critérios de qualidade:**
- Squads funcionam
- Colaboração entre mentes
- Debrief gera insights

---

#### 4.2 Hibridização Avançada
- [ ] Implementar hibridização ponderada
- [ ] Implementar hibridização contextual
- [ ] Implementar hibridização dinâmica
- [ ] Testes de hibridização

**Critérios de qualidade:**
- Hibridização ponderada funciona
- Hibridização contextual funciona
- Hibridização dinâmica funciona

---

## CAMADA 5: TESTES E DOCUMENTAÇÃO

### Objetivo
Garantir qualidade e documentação perfeitas

### O que deve ser feito

#### 5.1 Testes Automatizados
- [ ] Unit tests para todos os módulos
- [ ] Integration tests para cada camada
- [ ] E2E tests para workflows completos
- [ ] Coverage > 80%
- [ ] CI/CD configurado

**Critérios de qualidade:**
- Todos os módulos têm testes
- Integration tests funcionam
- E2E tests funcionam
- Coverage > 80%
- CI/CD executa testes

---

#### 5.2 Documentação
- [ ] README.md em cada módulo
- [ ] Examples em cada módulo
- [ ] API docs para todos os endpoints
- [ ] Tutorial de uso completo
- [ ] Troubleshooting guide

**Critérios de qualidade:**
- Todos os módulos têm README
- Examples funcionam
- API docs completas
- Tutorial cobre tudo
- Troubleshooting útil

---

## 🎯 REGRAS DE EXECUÇÃO

### 1. **COMPLETUDE POR CAMADA**
- Uma camada não começa até a anterior estar 100% completa
- Camada 0 → Camada 1 → Camada 2 → Camada 3 → Camada 4 → Camada 5

### 2. **CRITÉRIOS DE QUALIDADE**
- Cada item só é marcado como "feito" quando atinge TODOS os critérios de qualidade
- Não há "bom o suficiente" — é 100% ou 0%

### 3. **TESTES ANTES DE CÓDIGO**
- Escrever tests antes de implementar (TDD)
- Se não há tests, não há implementação

### 4. **DOCUMENTAÇÃO VIVA**
- PRDs são atualizados conforme implementação
- READMEs são atualizados a cada mudança
- Examples sempre funcionam

### 5. **OBSERVABILIDADE NATIVA**
- Logs em tudo
- Métricas em tudo
- Health checks em tudo

---

*Roadmap v1.0 — Foco: O QUE fazer, não QUANDO*
*Princípio: Qualidade sobre velocidade*
