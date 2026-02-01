# BRAINSTORM REGRAS DO RAG DINÂMICO

**Data:** 2026-01-31
**Status:** Brainstorm em progresso
**Objetivo:** Listar TODAS as regras específicas do RAG Dinâmico

---

## 📋 CATEGORIAS DE REGRAS DO RAG

### 1. **REGRAS DE EMBEDDINGS** (criação, atualização, versão)
### 2. **REGRAS DE BUSCA** (como recuperar, o que priorizar)
### 3. **REGRAS DE FRESHNESS** (o que é atual, o que é obsoleto)
### 4. **REGRAS DE MIGRAÇÃO** (quando migrar, como migrar)
### 5. **REGRAS DE QUALIDADE** (quão bom precisa ser)
### 6. **REGRAS DE PERFORMANCE** (tempo, limites, concorrência)
### 7. **REGRAS DE CONSERVAÇÃO** (o que manter, o que remover)

---

## 1️⃣ REGRAS DE EMBEDDINGS

### **Criação**
- 📌 **R-RAG-E-01**: Cria embedding automaticamente quando artefato é criado
- 📌 **R-RAG-E-02**: Usa modelo `text-embedding-3-small` por padrão
- 📌 **R-RAG-E-03**: Calcula embedding do **texto completo** do artefato
- 📌 **R-RAG-E-04**: Salva metadados (author, type, created_at, version)
- 📌 **R-RAG-E-05**: Se falhar ao criar embedding → Alerta, retry 3x, depois marca como "failed"

### **Atualização**
- 📌 **R-RAG-E-06**: Atualiza embedding automaticamente quando artefato é atualizado
- 📌 **R-RAG-E-07**: Incrementa versão do embedding (v1 → v2 → v3)
- 📌 **R-RAG-E-08**: Mantém histórico das últimas 5 versões
- 📌 **R-RAG-E-09**: Se falhar ao atualizar → Alerta, usa versão anterior, requeue para atualizar depois
- 📌 **R-RAG-E-10**: Se atualização falhar 3x → Marca embedding como "degraded", mas continua usando versão anterior

### **Remoção**
- 📌 **R-RAG-E-11**: Remove embedding automaticamente quando artefato é deletado
- 📌 **R-RAG-E-12**: Arquiva histórico de versões (não deleta) para rollback
- 📌 **R-RAG-E-13**: Se falhar ao remover → Logga, mas não para operação (non-blocking)

### **Batch**
- 📌 **R-RAG-E-14**: Processa embeddings em lotes de 100 (para otimizar)
- 📌 **R-RAG-E-15**: Se processamento batch falha → Re-tenta o lote, não todo
- 📌 **R-RAG-E-16**: Se lote falha 3x → Processa um a um, logga quais falharam

---

## 2️⃣ REGRAS DE BUSCA

### **Recuperação**
- 📌 **R-RAG-B-01**: Busca por similaridade coseno (padrão)
- 📌 **R-RAG-B-02**: Retorna top 10 resultados por padrão
- 📌 **R-RAG-B-03**: Se query < 3 palavras → Expande com sinônimos antes de buscar
- 📌 **R-RAG-B-04**: Se query é muito específica → Busca por exata + similaridade
- 📌 **R-RAG-B-05**: Timeout de busca: 5 segundos (padrão)

### **Priorização**
- 📌 **R-RAG-B-06**: Prioriza embeddings com `freshness_score > 0.8`
- 📌 **R-RAG-B-07**: Prioriza embeddings de autores canônicos
- 📌 **R-RAG-B-08**: Prioriza artefatos com `confidence > 0.8`
- 📌 **R-RAG-B-09**: Se prefer_fresh=true → Filtra embeddings obsoletos (freshness < 0.5)
- 📌 **R-RAG-B-10**: Se prefer_confidence=true → Filtra embeddings com confidence < 0.6

### **Filtragem**
- 📌 **R-RAG-B-11**: Remove embeddings duplicados (similarity > 95%)
- 📌 **R-RAG-B-12**: Remove embeddings marcados como "failed" ou "degraded"
- 📌 **R-RAG-B-13**: Se query é temporal (ex: "últimas ideias de 2025") → Filtra por created_at
- 📌 **R-RAG-B-14**: Se query menciona autor específico → Filtra por author_id
- 📌 **R-RAG-B-15**: Se query menciona tipo de artefato → Filtra por type

### **Reranking**
- 📌 **R-RAG-B-16**: Re-ranqueia resultados com score híbrido (similaridade + freshness + confidence)
- 📌 **R-RAG-B-17**: Se há resultados muito similares → Dedupa, mantém o melhor
- 📌 **R-RAG-B-18**: Se há resultados de mesmo autor → Limita a 3 por autor (para diversidade)
- 📌 **R-RAG-B-19**: Se busca não retorna resultados → Expande query (sinônimos, variantes) e re-busca
- 📌 **R-RAG-B-20**: Se busca retorna < 3 resultados → Relaxa filtros (thresholds)

---

## 3️⃣ REGRAS DE FRESHNESS

### **Freshness Score**
- 📌 **R-RAG-F-01**: `freshness_score = 1.0` quando embedding é criado
- 📌 **R-RAG-F-02**: `freshness_score` decai 0.05 por dia (padrão)
- 📌 **R-RAG-F-03**: Se embedding é atualizado → `freshness_score` volta para 1.0
- 📌 **R-RAG-F-04**: Se `freshness_score < 0.5` → Marca como "obsoleto"
- 📌 **R-RAG-F-05**: Se `freshness_score < 0.3` → Marca como "archived"

### **Detecção de Obsoletos**
- 📌 **R-RAG-F-06**: Verifica obsoletos automaticamente a cada 24h
- 📌 **R-RAG-F-07**: Se embedding não atualizado em > 30 dias → Marca como obsoleto
- 📌 **R-RAG-F-08**: Se embedding não atualizado em > 60 dias → Marca como archived
- 📌 **R-RAG-F-09**: Se embedding de autor ativo não atualizado em > 7 dias → Alerta (possível erro)
- 📌 **R-RAG-F-10**: Se embedding de projeto ativo não atualizado em > 14 dias → Alerta

### **Atualização de Freshness**
- 📌 **R-RAG-F-11**: Se artefato é atualizado → Atualiza embedding freshness para 1.0
- 📌 **R-RAG-F-12**: Se busca retorna embeddings obsoletos → Re-embeda automaticamente
- 📌 **R-RAG-F-13**: Se projeto é reativado → Atualiza freshness de todos os embeddings do projeto
- 📌 **R-RAG-F-14**: Se autor é reativado → Atualiza freshness de todos os embeddings do autor

---

## 4️⃣ REGRAS DE MIGRAÇÃO

### **Quando Migrar**
- 📌 **R-RAG-M-01**: Se modelo de embedding muda → Migra todos os embeddings automaticamente
- 📌 **R-RAG-M-02**: Se schema de embeddings muda → Migra todos os embeddings automaticamente
- 📌 **R-RAG-M-03**: Se ChromaDB versão muda → Verifica compatibilidade, migra se necessário
- 📌 **R-RAG-M-04**: Se embedding corrompido (checksum falha) → Re-gera do artefato original

### **Como Migrar**
- 📌 **R-RAG-M-05**: Antes de migrar → Faz backup completo de todos os embeddings
- 📌 **R-RAG-M-06**: Migra em lotes de 100 (para otimizar)
- 📌 **R-RAG-M-07**: Se migração falha para lote → Re-tenta esse lote, não todo
- 📌 **R-RAG-M-08**: Se lote falha 3x → Re-embeada um a um, logga quais falharam
- 📌 **R-RAG-M-09**: Se migração completa mas alguns falharam → Continua operacional, alerta sobre falhados
- 📌 **R-RAG-M-10**: Se migração falha críticamente → Rollback para backup

### **Validação Pós-Migração**
- 📌 **R-RAG-M-11**: Após migração → Valida que todos os embeddings foram migrados
- 📌 **R-RAG-M-12**: Valida que modelo atual está correto
- 📌 **R-RAG-M-13**: Valida que checksums batem (integridade)
- 📌 **R-RAG-M-14**: Faz busca de teste → Verifica que resultados são coerentes
- 📌 **R-RAG-M-15**: Se validação falha → Rollback para backup

### **Rollback**
- 📌 **R-RAG-M-16**: Se migração falha → Rollback para backup automático
- 📌 **R-RAG-M-17**: Se rollback falha → Alerta crítico, sistema em modo degradado
- 📌 **R-RAG-M-18**: Se rollback bem-sucedido → Re-migra manualmente (requer intervenção)

---

## 5️⃣ REGRAS DE QUALIDADE

### **Qualidade de Embeddings**
- 📌 **R-RAG-Q-01**: Se embedding falhou → Marca como "failed", não usa em buscas
- 📌 **R-RAG-Q-02**: Se embedding tem `NaN` ou `Inf` → Marca como "invalid", re-embeda
- 📌 **R-RAG-Q-03**: Se embedding tem dimensão incorreta → Marca como "invalid", re-embeda
- 📌 **R-RAG-Q-04**: Se embedding tem magnitude muito alta → Normaliza, logga
- 📌 **R-RAG-Q-05**: Se embedding tem magnitude muito baixa → Logga (possível conteúdo vazio)

### **Qualidade de Artefatos**
- 📌 **R-RAG-Q-06**: Se artefato sem `text_content` → Não embeeda
- 📌 **R-RAG-Q-07**: Se artefato com `text_length < 10` → Não embeeda (insuficiente)
- 📌 **R-RAG-Q-08**: Se artefato marcado como spam → Não embeeda
- 📌 **R-RAG-Q-09**: Se artefato com `quality_score < 0.3` → Não embeeda
- 📌 **R-RAG-Q-10**: Se artefato atualizado → Re-embeada automaticamente

### **Qualidade de Buscas**
- 📌 **R-RAG-Q-11**: Se busca retorna 0 resultados → Expande query e re-busca
- 📌 **R-RAG-Q-12**: Se busca retorna < 3 resultados → Relaxa filtros
- 📌 **R-RAG-Q-13**: Se busca retorna resultados muito similares (similarity > 98%) → Dedupa
- 📌 **R-RAG-Q-14**: Se busca toma > 5s → Timeout, alerta performance
- 📌 **R-RAG-Q-15**: Se busca retorna resultados de baixa qualidade (similarity < 0.6) → Logga

---

## 6️⃣ REGRAS DE PERFORMANCE

### **Timeouts**
- 📌 **R-RAG-P-01**: Timeout de criação de embedding: 30s (padrão)
- 📌 **R-RAG-P-02**: Timeout de atualização de embedding: 30s (padrão)
- 📌 **R-RAG-P-03**: Timeout de busca: 5s (padrão)
- 📌 **R-RAG-P-04**: Timeout de migração de lote: 60s (padrão)

### **Concorrência**
- 📌 **R-RAG-P-05**: Máximo de 10 embeddings paralelos (padrão)
- 📌 **R-RAG-P-06**: Máximo de 20 buscas paralelas (padrão)
- 📌 **R-RAG-P-07**: Máximo de 5 migrações paralelas (padrão)

### **Limites**
- 📌 **R-RAG-P-08**: Máximo de 10,000 embeddings por busca (segurança)
- 📌 **R-RAG-P-09**: Máximo de 100 embeddings por lote
- 📌 **R-RAG-P-10**: Máximo de 1,000 embeddings por minuto (rate limit)
- 📌 **R-RAG-P-11**: Se atingir limites → Queue, alerta, mas não falha

### **Cache**
- 📌 **R-RAG-P-12**: Cache de buscas: TTL de 10min (padrão)
- 📌 **R-RAG-P-13**: Cache de embeddings populares: TTL de 1h (padrão)
- 📌 **R-RAG-P-14**: LRU para cache (remove menos usado quando cheio)

---

## 7️⃣ REGRAS DE CONSERVAÇÃO

### **Retenção**
- 📌 **R-RAG-C-01**: Mantém embeddings ativos indefinidamente
- 📌 **R-RAG-C-02**: Mantém histórico de versões por 90 dias
- 📌 **R-RAG-C-03**: Remove embeddings "archived" após 180 dias
- 📌 **R-RAG-C-04**: Remove backups de migração após 30 dias
- 📌 **R-RAG-C-05**: Remove embeddings de projetos deletados após 30 dias

### **Limpeza**
- 📌 **R-RAG-C-06**: Limpeza de embeddings obsoletos a cada 7 dias
- 📌 **R-RAG-C-07**: Limpeza de histórico de versões a cada 30 dias
- 📌 **R-RAG-C-08**: Limpeza de backups antigos a cada 30 dias
- 📌 **R-RAG-C-09**: Se limpeza falha → Alerta, não para operações
- 📌 **R-RAG-C-10**: Logga todas as limpezas com detalhes (o que foi removido, por quê)

### **Compromisso**
- 📌 **R-RAG-C-11**: Nunca remove embeddings sem backup ou archiving
- 📌 **R-RAG-C-12**: Nunca remove embeddings de autores canônicos (preservar para sempre)
- 📌 **R-RAG-C-13**: Nunca remove embeddings em uso (ativo em projeto)
- 📌 **R-RAG-C-14**: Se projeto está em uso → Bloqueia limpeza de embeddings do projeto
- 📌 **R-RAG-C-15**: Se autor está ativo → Bloqueia limpeza de embeddings do autor

---

## 📊 RESUMO DE REGRAS DO RAG

| Categoria | Regras |
|-----------|--------|
| **Embeddings** | 16 |
| **Busca** | 20 |
| **Freshness** | 14 |
| **Migração** | 18 |
| **Qualidade** | 15 |
| **Performance** | 14 |
| **Conservação** | 15 |
| **TOTAL RAG** | **112** |

---

## 🎯 PRÓXIMOS PASSOS

Tio Bet, temos **112 REGRAS DO RAG** mapeadas!

**Opções:**
1. Integrar essas regras no PRD de RAG Dinâmico
2. Criar documento separado "REGRAS-RAG.md"
3. Codificar essas regras no RAG Engine (nascer com as regras no código)

**O que você prefere?** 🥷🏾
