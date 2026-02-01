# RegrasEngine — Motor de Execução de Regras

**Versão:** 1.0
**Data:** 2026-01-31

---

## 📋 Visão Geral

RegrasEngine é o motor central de execução de regras do ecossistema. Ele:
- Carrega regras de arquivos YAML
- Avalia condições em runtime
- Executa ações automaticamente
- Logga decisões para histórico
- Permite reload sem restart

### Módulos

| Módulo | Função | Arquivo |
|--------|--------|---------|
| **RegrasEngine** | Motor principal | `engine.py` |
| **RuleLoader** | Carrega YAML | `loader.py` |
| **ConditionParser** | Parser de condições | `parser.py` |
| **ActionExecutor** | Executa ações | `actions.py` |
| **RuleLogger** | Histórico de decisões | `logger.py` |

---

## 🚀 Uso Básico

### Inicialização

```python
from regras.engine import RegrasEngine

# Inicia engine (carrega regras automaticamente)
engine = RegrasEngine(rules_dir="rules")

print(f"Regras carregadas: {engine.count_rules()}")
```

### Avaliar Contexto

```python
# Define contexto
contexto = {
    "modulo": "rastreador",
    "sources_collected": 10000,
    "max_sources": 10000,
    "data_id": "source_001"
}

# Avalia regras
acoes = engine.evaluate(contexto)

print(f"Ações executadas: {len(acoes)}")
for acao in acoes:
    print(f"  - {acao['rule_id']}: {acao['acao']}")
```

### Buscar Regras

```python
# Por categoria
operacao_rules = engine.get_rules_by_category("operacao")
print(f"Regras de operação: {len(operacao_rules)}")

# Por módulo
rastreador_rules = engine.get_rules_by_module("rastreador")
print(f"Regras do rastreador: {len(rastreador_rules)}")
```

### Reload em Runtime

```python
# Recarrega regras sem restart
count = engine.reload()
print(f"Regras recarregadas: {count}")
```

---

## 📝 Formato de Regras

### Arquivo YAML

```yaml
# rules/ecossistema.yaml
regras:
  operacao:
    - id: R-OP-01
      modulo: rastreador
      categoria: operacao
      condicao: "sources_collected >= max_sources"
      acao: parar
      prioridade: alta
      descricao: Para quando atinge max_sources

    - id: R-OP-02
      modulo: rastreador
      categoria: operacao
      condicao: "sources_per_hour < 10"
      acao: parar
      prioridade: alta
      descricao: Para quando min_new_sources_per_hour < 10

  qualidade:
    - id: R-QF-01
      modulo: rastreador
      categoria: qualidade
      condicao: "quality_score < 0.7"
      acao: rejeitar
      prioridade: alta
      descricao: Rejeita fontes com quality < 0.7
```

### Campos Obrigatórios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | ID único da regra (ex: R-OP-01) |
| `modulo` | string | Módulo afetado (rastreador, minerador, loop, etc.) |
| `categoria` | string | Categoria (operacao, qualidade, decisao, etc.) |
| `condicao` | string | Condição em formato string |
| `acao` | string | Ação a executar |

### Campos Opcionais

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `prioridade` | string | alta, normal, baixa (padrão: normal) |
| `descricao` | string | Descrição da regra |
| `max_retries` | int | Máximo de retentativas (para retry_com_backoff) |

---

## 🔧 Condições Suportadas

### Operadores de Comparação

| Operador | Exemplo | Descrição |
|----------|---------|-----------|
| `>=` | `x >= y` | Maior ou igual |
| `<=` | `x <= y` | Menor ou igual |
| `>` | `x > y` | Maior que |
| `<` | `x < y` | Menor que |
| `==` | `x == y` | Igual |
| `!=` | `x != y` | Diferente |
| `in` | `x in [a, b, c]` | Contém em lista |
| `not in` | `x not in [a, b, c]` | Não contém em lista |

### Exemplos de Condições

```python
# Simples
"sources_collected >= 10000"
"quality_score < 0.7"

# Notação de ponto
"metrics.confidence_mean < 0.7"
"data.sources.length > 100"

# in / not in
"tag in ['video', 'youtube']"
"status not in ['deleted', 'archived']"

# Booleano
"artifact_created == true"
"is_spam == true"
```

---

## ⚡ Ações Disponíveis

| Ação | Descrição | Parâmetros Adicionais |
|-------|-----------|----------------------|
| `parar` | Para módulo | Nenhum |
| `rejeitar` | Rejeita dado | Nenhum |
| `retry_com_backoff` | Retry com backoff | `max_retries` |
| `alert` | Envia alerta | Nenhum |
| `create_embedding` | Cria embedding | Nenhum |
| `update_embedding` | Atualiza embedding | Nenhum |
| `mark_obsolete` | Marca obsoleto | Nenhum |

### Exemplos de Ações

```python
# Ação: parar
condicao: "sources_collected >= max_sources"
acao: parar
resultado: {"status": "stopped", "modulo": "rastreador"}

# Ação: rejeitar
condicao: "quality_score < 0.7"
acao: rejeitar
resultado: {"status": "rejected", "data_id": "source_001"}

# Ação: retry_com_backoff
condicao: "error_type == transient"
acao: retry_com_backoff
max_retries: 3
resultado: {"status": "retrying", "wait_time": 1.0, "new_retry_count": 1}

# Ação: alert
condicao: "error_type == permanent"
acao: alert
resultado: {"status": "alert_sent", "rule_id": "R-D-03"}
```

---

## 🗄️ Histórico de Decisões

RegrasEngine logga todas as decisões em SQLite (`rule_decisions.db`).

### Estrutura da Tabela

```sql
CREATE TABLE decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    rule_set TEXT NOT NULL,
    modulo TEXT NOT NULL,
    condicao TEXT NOT NULL,
    acao TEXT,
    contexto TEXT,
    resultado TEXT
)
```

### Consultar Histórico

```python
from regras.logger import RuleLogger

logger = RuleLogger()

# Histórico completo
history = logger.get_history(limit=10)
for decision in history:
    print(f"{decision[1]} - {decision[3]}: {decision[6]}")

# Histórico de uma regra
history = logger.get_history(rule_id="R-OP-01", limit=20)
```

---

## 🧮 Priorização

Ações são ordenadas por prioridade:
- `alta` (score 3)
- `normal` (score 2)
- `baixa` (score 1)

### Exemplo

```python
contexto = {
    "modulo": "rastreador",
    "sources_collected": 10000,
    "max_sources": 10000,
    "quality_score": 0.5
}

acoes = engine.evaluate(contexto)

# Ações ordenadas por prioridade
# 1. R-QF-01: rejeitar (alta)
# 2. R-OP-01: parar (alta)
# 3. R-P-09: prioritize (alta)
```

---

## 🧪 Exemplos Completos

### Exemplo 1: Rastreador com Critérios de Parada

```python
from regras.engine import RegrasEngine

engine = RegrasEngine()

# Loop de coleta
while True:
    # Coleta batch
    sources = collect_batch()
    sources_collected = len(sources)

    # Avalia regras
    contexto = {
        "modulo": "rastreador",
        "sources_collected": sources_collected,
        "max_sources": 10000,
        "sources_per_hour": len(sources) / 3600,
        "quality_score": calculate_quality(sources),
        "data_id": None
    }

    acoes = engine.evaluate(contexto)

    # Se há ação "parar", encerra
    if any(a["acao"] == "parar" for a in acoes):
        print("Critérios de parada atendidos!")
        break

    # Continua coleta
    sleep(60)
```

### Exemplo 2: Validação de Qualidade

```python
from regras.engine import RegrasEngine

engine = RegrasEngine()

# Valida dado
data = {"id": "source_001", "text": "..."}
quality_score = calculate_quality(data)

contexto = {
    "modulo": "rastreador",
    "data_id": data["id"],
    "quality_score": quality_score,
    "is_spam": check_spam(data),
    "duration": data.get("duration", 0),
    "text_length": len(data.get("text", ""))
}

acoes = engine.evaluate(contexto)

# Se há ação "rejeitar", rejeita
if any(a["acao"] == "rejeitar" for a in acoes):
    print("Dado rejeitado por regra de qualidade")
    return False

# Passou validação
print("Dado aprovado")
return True
```

### Exemplo 3: Tratamento de Erros

```python
from regras.engine import RegrasEngine

engine = RegrasEngine()

def process_with_retry(data, retry_count=0):
    try:
        # Tenta processar
        result = process(data)
        return result

    except Exception as e:
        error_type = classify_error(e)

        # Avalia regras
        contexto = {
            "modulo": "geral",
            "error_type": error_type,
            "retry_count": retry_count
        }

        acoes = engine.evaluate(contexto)

        # Verifica se deve retry
        retry_action = next((a for a in acoes if a["acao"] == "retry_com_backoff"), None)

        if retry_action and retry_action["result"]["status"] == "retrying":
            wait_time = retry_action["result"]["wait_time"]
            new_retry_count = retry_action["result"]["new_retry_count"]

            print(f"Retry em {wait_time}s...")

            # Espera e retry
            sleep(wait_time)
            return process_with_retry(data, new_retry_count)

        # Não retry, lança exceção
        raise e
```

---

## 📚 Referência de API

### RegrasEngine

```python
class RegrasEngine:
    def __init__(self, rules_dir: str = "rules")
    def load_all_rules(self) -> None
    def evaluate(self, contexto: Dict[str, Any]) -> List[Dict[str, Any]]
    def reload(self) -> Dict[str, int]
    def count_rules(self) -> int
    def get_rules_by_category(self, category: str) -> List[Dict[str, Any]]
    def get_rules_by_module(self, module: str) -> List[Dict[str, Any]]
```

### RuleLoader

```python
class RuleLoader:
    def __init__(self, path: str)
    def load(self) -> dict
    def validate_schema(self, data: dict) -> None
```

### ConditionParser

```python
class ConditionParser:
    def parse_and_eval(self, condition: str, contexto: dict) -> bool
    def has_comparator(self, condition: str) -> bool
    def parse(self, condition: str) -> tuple
    def resolve_variable(self, var: str, contexto: dict)
    def eval_comparison(self, left, op: str, right) -> bool
```

### ActionExecutor

```python
class ActionExecutor:
    def __init__(self)
    def execute(self, action_name: str, rule: dict, contexto: dict) -> dict
    def action_parar(self, rule: dict, contexto: dict) -> dict
    def action_rejeitar(self, rule: dict, contexto: dict) -> dict
    def action_retry_com_backoff(self, rule: dict, contexto: dict) -> dict
    def action_alert(self, rule: dict, contexto: dict) -> dict
    # ... outras ações
```

### RuleLogger

```python
class RuleLogger:
    def __init__(self)
    def log(self, rule: dict, contexto: dict, resultado: dict) -> None
    def get_history(self, rule_id: str = None, limit: int = 100) -> list
```

---

## 🎯 Práticas Recomendadas

### 1. Contexto Completo
Sempre passe todas as variáveis que as regras podem precisar:

```python
# ✅ Bom - contexto completo
contexto = {
    "modulo": "rastreador",
    "sources_collected": 10000,
    "max_sources": 10000,
    "sources_per_hour": 50,
    "quality_score": 0.8,
    "is_spam": False,
    "data_id": "source_001"
}

# ❌ Ruim - contexto incompleto
contexto = {
    "modulo": "rastreador",
    "sources_collected": 10000
}
```

### 2. IDs de Regras Únicos
Use prefixos consistentes:

```yaml
# ✅ Bom - prefixos consistentes
- id: R-OP-01
- id: R-QF-01
- id: R-D-01

# ❌ Ruim - sem padrão
- id: rule1
- id: parar_rastreador
- id: rejeitar_spam
```

### 3. Descrições Claras
Descreva o que a regra faz:

```yaml
# ✅ Bom - descrição clara
descricao: Para quando atinge max_sources

# ❌ Ruim - descrição vaga
descricao: Parar
```

---

## 🚨 Erros Comuns

### Error: No module named 'yaml'
**Solução:** Instale PyYAML
```bash
pip install pyyaml
```

### Error: mapping values are not allowed here
**Causa:** Erro de sintaxe no YAML
**Solução:** Verifique indentação e caracteres especiais

### Error: AttributeError: 'str' object has no attribute 'get'
**Causa:** Contexto não é um dict
**Solução:** Passe contexto como dict

---

## 📞 Suporte

- **Código:** `src/regras/`
- **Regras:** `rules/`
- **Testes:** `test_regras_standalone.py`
- **Documentação:** Este arquivo

---

*RegrasEngine v1.0 — Documentado em 2026-01-31*
