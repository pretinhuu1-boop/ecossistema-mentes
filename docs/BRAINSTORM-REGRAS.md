# BRAINSTORM REGRAS DO ECOSSISTEMA

**Data:** 2026-01-31
**Status:** Brainstorm em progresso
**Objetivo:** Listar TODAS as regras que o ecossistema precisa

---

## 🎯 O QUE SÃO "REGRAS"?

**Regras** = Lógica de decisão + Critérios + Thresholds + Comportamento esperado

**Diferença de PRDs:**
- **PRDs** = Como funciona (implementação)
- **Regras** = O que fazer (decisão)

---

## 📋 CATEGORIAS DE REGRAS

### 1. **REGRAS DE OPERAÇÃO** (Quando parar, como proceder)
### 2. **REGRAS DE QUALIDADE** (Quão bom precisa ser)
### 3. **REGRAS DE DECISÃO** (Retry ou abort? Processar ou ignorar?)
### 4. **REGRAS DE PRIORIZAÇÃO** (O que fazer primeiro?)
### 5. **REGRAS DE SEGURANÇA** (O que evitar)
### 6. **REGRAS DE PERFORMANCE** (Limites, timeouts)
### 7. **REGRAS DE CONVERGÊNCIA** (Quando é "bom o suficiente"?)
### 8. **REGRAS DE MANUTENÇÃO** (Quando atualizar, quando limpar)

---

## 1️⃣ REGRAS DE OPERAÇÃO

### **Rastreador**
- 📌 **R-OP-01**: Rastreador para quando atinge `max_sources` (padrão: 10,000)
- 📌 **R-OP-02**: Rastreador para quando `min_new_sources_per_hour < 10` (padrão: 10)
- 📌 **R-OP-03**: Rastreador para quando `max_hours_without_new > 4` (padrão: 4h)
- 📌 **R-OP-04**: Rastreador para quando `completeness_threshold >= 0.95` (padrão: 95%)

### **Minerador**
- 📌 **R-OP-05**: Minerador para quando `max_artifacts_per_source > 100` (padrão: 100)
- 📌 **R-OP-06**: Minerador para quando `min_confidence_mean < 0.7` (padrão: 0.7)
- 📌 **R-OP-07**: Minerador para quando `max_hours_without_new > 2` (padrão: 2h)
- 📌 **R-OP-08**: Minerador para quando `saturation_threshold >= 0.9` (padrão: 90%)

### **Loop de Qualidade**
- 📌 **R-OP-09**: Loop para quando `max_iterations > 10` (padrão: 10)
- 📌 **R-OP-10**: Loop para quando `min_improvement_per_iteration < 0.01` (padrão: 1%)
- 📌 **R-OP-11**: Loop para quando `max_hours_without_improvement > 6` (padrão: 6h)
- 📌 **R-OP-12**: Loop para quando detecta oscilação (diferença < 5% entre iterações)

### **Orquestrador**
- 📌 **R-OP-13**: Orquestrador para todas as filas quando `queue_empty_threshold > 5min`
- 📌 **R-OP-14**: Orquestrador alerta quando `failed_tasks > 10%` em 1h
- 📌 **R-OP-15**: Orquestrador escala workers quando `queue_pending > 1000`

---

## 2️⃣ REGRAS DE QUALIDADE

### **Fontes (Rastreador)**
- 📌 **R-QF-01**: Rejeita fontes com `quality_score < 0.7` (padrão: 0.7)
- 📌 **R-QF-02**: Rejeita fontes marcadas como spam
- 📌 **R-QF-03**: Rejeita fontes com `duration < 30s` (vídeo/áudio)
- 📌 **R-QF-04**: Rejeita fontes com `text_length < 100 caracteres`
- 📌 **R-QF-05**: Rejeita fontes com `repetition > 30%`

### **Artefatos (Minerador)**
- 📌 **R-QA-01**: Rejeita artefatos com `confidence < 0.5` (padrão: 0.5)
- 📌 **R-QA-02**: Rejeita artefatos sem `author_context`
- 📌 **R-QA-03**: Rejeita artefatos duplicados (similarity > 95%)
- 📌 **R-QA-04**: Rejeita artefatos sem `text_content`
- 📌 **R-QA-05**: Rejeita artefatos com `context_depth < 2` (muito superficial)

### **Mentes (Construtor)**
- 📌 **R-QM-01**: Rejeita mentes com `artifacts_count < 50` (padrão: 50)
- 📌 **R-QM-02**: Rejeita mentes com `signature_coherence < 0.6` (padrão: 0.6)
- 📌 **R-QM-03**: Rejeita mentes sem `biases` identificados
- 📌 **R-QM-04**: Rejeita mentes sem `voice_patterns` identificados
- 📌 **R-QM-05**: Rejeita mentes com `coverage < 0.7` (cobertura de tópicos)

### **Embeddings (RAG)**
- 📌 **R-QE-01**: Prioriza embeddings com `freshness_score > 0.8` em buscas
- 📌 **R-QE-02**: Marca embeddings como obsoletos se `updated_at > 30 dias`
- 📌 **R-QE-03**: Re-embeda artefatos atualizados automaticamente
- 📌 **R-QE-04**: Re-embeda todos se mudar modelo de embedding

---

## 3️⃣ REGRAS DE DECISÃO

### **Tratamento de Erros**
- 📌 **R-D-01**: Erros **transientes** (timeout, network) → Retry com backoff exponencial (max 3x)
- 📌 **R-D-02**: Erros **rate limit** → Espera `retry_after` segundos, depois retry (max 5x)
- 📌 **R-D-03**: Erros **permanentes** (404, 403) → Aborta, alerta, não retry
- 📌 **R-D-04**: Erros **desconhecidos** → Alerta crítico, aborta

### **Duplicados**
- 📌 **R-D-05**: Conteúdo duplicado (similarity > 95%) → Ignora, mantém primeira ocorrência
- 📌 **R-D-06**: Conteúdo near-duplicate (similarity 80-95%) → Logga, processa como "variante"
- 📌 **R-D-07**: Artefato duplicado → Ignora, mantém versão com maior confidence

### **Spam**
- 📌 **R-D-08**: Conteúdo spam (score > 0.5) → Rejeita, logga
- 📌 **R-D-09**: Fonte com múltiplos spams → Marca fonte como "suspensa", ignora futuras
- 📌 **R-D-10**: Autor com alta taxa de spam → Reduz prioridade de fontes desse autor

### **Saúde do Sistema**
- 📌 **R-D-11**: Se Redis down → Para todas as operações, alerta crítico
- 📌 **R-D-12**: Se Celery sem workers → Para enfileiramento, alerta crítico
- 📌 **R-D-13**: Se ChromaDB down → Para buscas, alerta crítico, mas continua processamento
- 📌 **R-D-14**: Se memória RAM > 90% → Para novos processamentos, alerta
- 📌 **R-D-15**: Se disco < 10% livre → Para tudo, alerta crítico

---

## 4️⃣ REGRAS DE PRIORIZAÇÃO

### **Filas**
- 📌 **R-P-01**: Fontes canônicas → Fila ALTA (livros, vídeos principais)
- 📌 **R-P-02**: Fontes regulares → Fila NORMAL (artigos, podcasts)
- 📌 **R-P-03**: Fontes exploratórias → Fila BAIXA (buscas secundárias)
- 📌 **R-P-04**: Artefatos com `confidence > 0.9` → Fila ALTA para construção
- 📌 **R-P-05**: Artefatos com `confidence < 0.7` → Fila BAIXA (só processar se tempo livre)

### **Buscas**
- 📌 **R-P-06**: Prioriza embeddings `freshness_score > 0.8`
- 📌 **R-P-07**: Prioriza artefatos de autores canônicos
- 📌 **R-P-08**: Prioriza artefatos com mais `context_depth`

### **Projects**
- 📌 **R-P-09**: Projetos ativos → Processamento prioritário
- 📌 **R-P-10**: Projetos em background → Processamento quando recursos livres

---

## 5️⃣ REGRAS DE SEGURANÇA

### **Dados**
- 📌 **R-S-01**: NUNCA exponha dados pessoais sem permissão
- 📌 **R-S-02**: Criptografa dados sensíveis em repouso
- 📌 **R-S-03**: Backups diários automáticos
- 📌 **R-S-04**: Retém backups por 30 dias (padrão)
- 📌 **R-S-05**: Integridade de dados verificada a cada 24h

### **API**
- 📌 **R-S-06**: Rate limiting: 100 req/min por IP (padrão)
- 📌 **R-S-07**: Autenticação obrigatória para operações de escrita
- 📌 **R-S-08**: Logs de todas as operações sensíveis

### **Scraping**
- 📌 **R-S-09**: Respeita `robots.txt`
- 📌 **R-S-10**: Respeita rate limits de APIs externas
- 📌 **R-S-11**: User-Agent honesto (não spoof)
- 📌 **R-S-12**: Intervalo mínimo entre requests (padrão: 1s)

---

## 6️⃣ REGRAS DE PERFORMANCE

### **Timeouts**
- 📌 **R-PF-01**: Timeout de scraping: 30s (padrão)
- 📌 **R-PF-02**: Timeout de extração de artefatos: 60s (padrão)
- 📌 **R-PF-03**: Timeout de construção de mente: 5min (padrão)
- 📌 **R-PF-04**: Timeout de busca RAG: 5s (padrão)

### **Concorrência**
- 📌 **R-PF-05**: Máximo de workers Celery: 8 (padrão)
- 📌 **R-PF-06**: Máximo de requests paralelos de scraping: 5 (padrão)
- 📌 **R-PF-07**: Máximo de builds paralelos de mente: 3 (padrão)

### **Limites**
- 📌 **R-PF-08**: Máximo de fontes por projeto: 100,000 (padrão)
- 📌 **R-PF-09**: Máximo de artefatos por mente: 10,000 (padrão)
- 📌 **R-PF-10**: Máximo de queries RAG por minuto: 60 (padrão)

---

## 7️⃣ REGRAS DE CONVERGÊNCIA

### **Loop de Qualidade**
- 📌 **R-C-01**: Loop converge quando melhoria < 1% em 2 iterações consecutivas
- 📌 **R-C-02**: Loop converge quando qualidade média >= 0.9 (padrão)
- 📌 **R-C-03**: Loop converge quando gaps < 3 (padrão)
- 📌 **R-C-04**: Loop converge quando todos os thresholds atingidos
- 📌 **R-C-05**: Loop aborta se oscila por > 3 iterações

### **Mentes**
- 📌 **R-C-06**: Mente está "completa" quando `coverage >= 0.95`
- 📌 **R-C-07**: Mente está "completa" quando `signature_coherence >= 0.9`
- 📌 **R-C-08**: Mente está "completa" quando `artifacts_count` não cresce por 24h

---

## 8️⃣ REGRAS DE MANUTENÇÃO

### **Limpeza**
- 📌 **R-M-01**: Remove logs > 30 dias automaticamente
- 📌 **R-M-02**: Remove eventos processados > 7 dias automaticamente
- 📌 **R-M-03**: Remove backups > 30 dias automaticamente
- 📌 **R-M-04**: Remove embeddings obsoletos (não atualizados > 60 dias) a cada 7 dias

### **Atualizações**
- 📌 **R-M-05**: Verifica integridade de dados a cada 24h
- 📌 **R-M-06**: Detecta embeddings obsoletos a cada 24h
- 📌 **R-M-07**: Verifica health checks a cada 5min
- 📌 **R-M-08**: Limpa cache de Redis a cada 1h (LRU)

### **Migrações**
- 📌 **R-M-09**: Migra embeddings automaticamente se modelo mudar (com backup)
- 📌 **R-M-10**: Migra estado do sistema se schema mudar (com backup)

---

## 📊 RESUMO DE REGRAS POR CATEGORIA

| Categoria | Regras |
|-----------|--------|
| **Operação** | 15 |
| **Qualidade** | 20 |
| **Decisão** | 15 |
| **Priorização** | 10 |
| **Segurança** | 12 |
| **Performance** | 10 |
| **Convergência** | 8 |
| **Manutenção** | 10 |
| **TOTAL** | **100** |

---

## 🎯 PRÓXIMOS PASSOS

Tio Bet, temos **100 REGRAS** mapeadas!

**Opções:**
1. Criar documento formal de regras (REGRAS-ECOSSISTEMA.md)
2. Criar PRD específico para "Regras do Ecossistema"
3. Integrar essas regras nos PRDs existentes
4. Criar módulo "RegrasEngine" que aplica essas regras

**O que você prefere?** 🥷🏾
