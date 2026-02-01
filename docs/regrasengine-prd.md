# REGRASENGINE — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 19)

---

## Problema

**Hoje:**
- 212 regras espalhadas em 18 PRDs
- Regras misturadas com implementação
- Mudar regra = re-deploy módulo (2-3 horas)

**Precisamos de:**
- Regras centralizadas em YAML/JSON
- Engine de execução de regras
- Regras editáveis sem re-deploy
- Regras testáveis isoladamente

---

## Stack Técnica

### Motor (Python)
- **Python** — Lógica de engine
- **PyYAML** — Parser de YAML
- **Jinja2** — Templates de condições (opcional)
- **SQLite** — Histórico de decisões

### Integração
- **Todos os módulos** — Consomem RegrasEngine
- **Orquestrador** — Dispara avaliações de regras

---

## Funcionalidades

### Core
- [ ] Loader de regras (YAML/JSON)
- [ ] Engine de execução de regras
- [ ] Parser de condições
- [ ] Executor de ações
- [ ] Logger de decisões
- [ ] Reload de regras em runtime

### Regras
- [ ] 212 regras mapeadas (100 gerais + 112 RAG)
- [ ] Regras em 2 arquivos YAML (ecossistema.yaml, rag.yaml)
- [ ] Regras customizáveis por projeto
- [ ] Versionamento de regras

### Testabilidade
- [ ] Testar regra isoladamente
- [ ] Simular contexto
- [ ] Verificar ação antes de executar

---

## Estrutura de Regras

### Regras do Ecossistema (rules/ecossistema.yaml)
```yaml
regras:
  operacao:
    - id: R-OP-01
      modulo: rastreador
      categoria: operacao
      condicao: "sources_collected >= max_sources"
      acao: "parar"
      prioridade: alta
      descricao: "Para quando atinge max_sources"

    - id: R-OP-02
      modulo: rastreador
      categoria: operacao
      condicao: "sources_per_hour < 10"
      acao: "parar"
      prioridade: alta
      descricao: "Para quando min_new_sources_per_hour < 10"

  qualidade:
    - id: R-QF-01
      modulo: rastreador
      categoria: qualidade
      condicao: "quality_score < 0.7"
      acao: "rejeitar"
      prioridade: alta
      descricao: "Rejeita fontes com quality < 0.7"

  decisao:
    - id: R-D-01
      modulo: geral
      categoria: decisao
      tipo_erro: "transient"
      acao: "retry_com_backoff"
      max_retries: 3
      prioridade: alta
      descricao: "Retry erros transientes com backoff"

# Configurações globais
configuracoes:
  max_sources: 10000
  min_new_sources_per_hour: 10
  quality_threshold: 0.7
  freshness_threshold: 0.8
```

### Regras do RAG (rules/rag.yaml)
```yaml
regras:
  embeddings:
    - id: R-RAG-E-01
      modulo: rag
      categoria: embeddings
      condicao: "artifact_created"
      acao: "create_embedding"
      prioridade: alta
      descricao: "Cria embedding automaticamente"

    - id: R-RAG-E-02
      modulo: rag
      categoria: embeddings
      condicao: "artifact_updated"
      acao: "update_embedding"
      prioridade: alta
      descricao: "Atualiza embedding automaticamente"

  busca:
    - id: R-RAG-B-06
      modulo: rag
      categoria: busca
      condicao: "search_query"
      acao: "prioritize_fresh"
      prioridade: normal
      descricao: "Prioriza embeddings com freshness > 0.8"

  freshness:
    - id: R-RAG-F-07
      modulo: rag
      categoria: freshness
      condicao: "embedding_age_days > 30"
      acao: "mark_obsolete"
      prioridade: alta
      descricao: "Marca obsoletos após 30 dias"
```

---

## RegrasEngine

```python
class RegrasEngine:
    def __init__(self, rules_dir="rules"):
        self.rules_dir = rules_dir
        self.rules = {}
        self.logger = RuleLogger()
        self.parser = ConditionParser()
        self.executor = ActionExecutor()

        # Carrega regras
        self.load_all_rules()

    def load_all_rules(self):
        """Carrega todas as regras do diretório"""
        rule_files = {
            "ecossistema": f"{self.rules_dir}/ecossistema.yaml",
            "rag": f"{self.rules_dir}/rag.yaml"
        }

        for name, path in rule_files.items():
            self.rules[name] = self.load_rules(path)

    def load_rules(self, path):
        """Carrega regras de um arquivo YAML"""
        loader = RuleLoader(path)
        return loader.load()

    def evaluate(self, contexto):
        """
        Avalia regras para um contexto específico

        Args:
            contexto: dict com {modulo, metrics, data_id, ...}

        Returns:
            list: Ações executadas
        """
        acoes_executadas = []

        # Para cada arquivo de regras
        for rule_set_name, rule_set in self.rules.items():
            # Filtra regras relevantes
            relevant_rules = self.filter_relevant(rule_set, contexto)

            # Avalia cada regra
            for rule in relevant_rules:
                # Avalia condição
                condition_met = self.parser.parse_and_eval(
                    rule["condicao"],
                    contexto
                )

                if condition_met:
                    # Executa ação
                    result = self.executor.execute(
                        rule["acao"],
                        rule,
                        contexto
                    )

                    # Logga
                    self.logger.log(rule, contexto, result)

                    # Coleta ação
                    acoes_executadas.append({
                        "rule_id": rule["id"],
                        "rule_set": rule_set_name,
                        "acao": rule["acao"],
                        "prioridade": rule.get("prioridade", "normal"),
                        "result": result
                    })

        # Ordena por prioridade
        acoes_executadas.sort(key=lambda x: self.prioridade_score(x["prioridade"]))

        return acoes_executadas

    def filter_relevant(self, rule_set, contexto):
        """Filtra regras relevantes para o contexto"""
        relevant = []

        for rule in rule_set.get("regras", []):
            # Filtra por módulo
            if rule.get("modulo") == contexto.get("modulo"):
                relevant.append(rule)
            elif rule.get("modulo") == "geral":
                relevant.append(rule)

        return relevant

    def prioridade_score(self, prioridade):
        """Converte prioridade para score numérico"""
        scores = {
            "alta": 3,
            "normal": 2,
            "baixa": 1
        }
        return scores.get(prioridade, 2)

    def reload(self):
        """Recarrega regras em runtime"""
        print("Recarregando regras...")
        self.load_all_rules()
        print(f"Regras recarregadas: {self.count_rules()}")
```

---

## RuleLoader

```python
class RuleLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        """Carrega regras do arquivo YAML"""
        with open(self.path, 'r') as f:
            data = yaml.safe_load(f)

        # Valida esquema
        self.validate_schema(data)

        return data

    def validate_schema(self, data):
        """Valida esquema de regras"""
        # Verifica se tem "regras"
        if "regras" not in data:
            raise RuleSchemaError("Arquivo deve conter 'regras'")

        # Verifica se cada regra tem campos obrigatórios
        for category, rules in data["regras"].items():
            for rule in rules:
                required_fields = ["id", "modulo", "categoria", "condicao", "acao"]

                for field in required_fields:
                    if field not in rule:
                        raise RuleSchemaError(
                            f"Regra {rule.get('id', 'unknown')} "
                            f"missing field: {field}"
                        )
```

---

## ConditionParser

```python
class ConditionParser:
    def parse_and_eval(self, condition, contexto):
        """
        Parser e avaliação de condições

        Args:
            condition: String de condição ("sources_collected >= max_sources")
            contexto: dict com contexto

        Returns:
            bool: Resultado da avaliação
        """
        # Se condição é simples (sem comparadores)
        if not self.has_comparator(condition):
            # Verifica se é True em contexto
            return contexto.get(condition, False)

        # Parse condição
        left, op, right = self.parse(condition)

        # Resolve variáveis
        left_value = self.resolve_variable(left, contexto)
        right_value = self.resolve_variable(right, contexto)

        # Avalia
        return self.eval_comparison(left_value, op, right_value)

    def has_comparator(self, condition):
        """Verifica se condição tem comparador"""
        return any(op in condition for op in [">=", "<=", ">", "<", "==", "!=", "in", "not in"])

    def parse(self, condition):
        """Parse condição em left, op, right"""
        comparators = [">=", "<=", ">", "<", "==", "!=", " in ", " not in "]

        for comp in comparators:
            if comp in condition:
                parts = condition.split(comp)
                if len(parts) == 2:
                    return parts[0].strip(), comp.strip(), parts[1].strip()

        raise ConditionParseError(f"Could not parse condition: {condition}")

    def resolve_variable(self, var, contexto):
        """Resolve variável do contexto"""
        # Se é número, retorna como número
        try:
            return float(var)
        except ValueError:
            pass

        # Se é string, busca em contexto
        return contexto.get(var, None)

    def eval_comparison(self, left, op, right):
        """Avalia comparação"""
        if op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        elif op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "in":
            return left in right
        elif op == "not in":
            return left not in right
        else:
            raise ConditionEvalError(f"Unknown operator: {op}")
```

---

## ActionExecutor

```python
class ActionExecutor:
    def __init__(self):
        self.actions = {
            "parar": self.action_parar,
            "rejeitar": self.action_rejeitar,
            "retry_com_backoff": self.action_retry_com_backoff,
            "create_embedding": self.action_create_embedding,
            "update_embedding": self.action_update_embedding,
            "mark_obsolete": self.action_mark_obsolete,
            "alert": self.action_alert
        }

    def execute(self, action_name, rule, contexto):
        """Executa ação"""
        action = self.actions.get(action_name)

        if not action:
            print(f"Ação desconhecida: {action_name}")
            return {"status": "unknown_action"}

        return action(rule, contexto)

    def action_parar(self, rule, contexto):
        """Ação: Parar módulo"""
        modulo = contexto["modulo"]

        print(f"🛑 Parando {modulo}: {rule['descricao']}")
        print(f"   Condição: {rule['condicao']}")

        # TODO: Implementar parada real
        # Stopper.stop(modulo)

        return {"status": "stopped", "modulo": modulo}

    def action_rejeitar(self, rule, contexto):
        """Ação: Rejeitar dado"""
        data_id = contexto.get("data_id")

        print(f"❌ Rejeitando {data_id}: {rule['descricao']}")
        print(f"   Condição: {rule['condicao']}")

        # TODO: Implementar rejeição real
        # RejectionMarker.mark(data_id)

        return {"status": "rejected", "data_id": data_id}

    def action_retry_com_backoff(self, rule, contexto):
        """Ação: Retry com backoff"""
        retry_count = contexto.get("retry_count", 0)
        max_retries = rule.get("max_retries", 3)

        if retry_count >= max_retries:
            print(f"❌ Máximo de retentativas atingido: {max_retries}")
            return {"status": "max_retries_exceeded"}

        # Calcula backoff
        wait_time = 2 ** retry_count

        print(f"🔄 Retry {retry_count + 1}/{max_retries} em {wait_time}s")

        # TODO: Implementar retry real
        # Backoff.wait(wait_time)

        return {
            "status": "retrying",
            "wait_time": wait_time,
            "new_retry_count": retry_count + 1
        }

    def action_create_embedding(self, rule, contexto):
        """Ação: Criar embedding"""
        artifact_id = contexto.get("artifact_id")

        print(f"📝 Criando embedding para {artifact_id}")

        # TODO: Integrar com RAG
        # EmbeddingManager.create(artifact_id)

        return {"status": "embedding_created", "artifact_id": artifact_id}

    def action_update_embedding(self, rule, contexto):
        """Ação: Atualizar embedding"""
        artifact_id = contexto.get("artifact_id")

        print(f"🔄 Atualizando embedding para {artifact_id}")

        # TODO: Integrar com RAG
        # EmbeddingManager.update(artifact_id)

        return {"status": "embedding_updated", "artifact_id": artifact_id}

    def action_mark_obsolete(self, rule, contexto):
        """Ação: Marcar embedding como obsoleto"""
        embedding_id = contexto.get("embedding_id")

        print(f"⚠️ Marcando {embedding_id} como obsoleto")

        # TODO: Integrar com RAG
        # EmbeddingManager.mark_obsolete(embedding_id)

        return {"status": "marked_obsolete", "embedding_id": embedding_id}

    def action_alert(self, rule, contexto):
        """Ação: Enviar alerta"""
        print(f"🚨 ALERTA: {rule['descricao']}")
        print(f"   Condição: {rule['condicao']}")

        # TODO: Integrar com AlertManager
        # AlertManager.send(rule, contexto)

        return {"status": "alert_sent"}
```

---

## RuleLogger

```python
class RuleLogger:
    def __init__(self):
        self.db = sqlite3.connect('rule_decisions.db')
        self.init_db()

    def init_db(self):
        """Inicializa banco de decisões"""
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                rule_set TEXT NOT NULL,
                modulo TEXT NOT NULL,
                condicao TEXT NOT NULL,
                acao TEXT NOT NULL,
                contexto TEXT,
                resultado TEXT
            )
        """)
        self.db.commit()

    def log(self, rule, contexto, resultado):
        """Logga decisão de regra"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO decisions (timestamp, rule_id, rule_set, modulo,
                                   condicao, acao, contexto, resultado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            rule["id"],
            rule.get("rule_set", "unknown"),
            rule["modulo"],
            rule["condicao"],
            rule["acao"],
            json.dumps(contexto),
            json.dumps(resultado)
        ))
        self.db.commit()

    def get_history(self, rule_id=None, limit=100):
        """Busca histórico de decisões"""
        cursor = self.db.cursor()

        query = "SELECT * FROM decisions"
        params = []

        if rule_id:
            query += " WHERE rule_id = ?"
            params.append(rule_id)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        return cursor.fetchall()
```

---

## Integração com Módulos

### Rastreador com RegrasEngine
```python
class RastreadorWithRegrasEngine:
    def __init__(self):
        self.engine = RegrasEngine()

    def collect_loop(self):
        """Loop de coleta com avaliação de regras"""
        while True:
            # Coleta
            metrics = self.collect_batch()

            # Avalia regras
            contexto = {
                "modulo": "rastreador",
                "metrics": metrics,
                "data_id": None,
                "sources_collected": metrics.get("sources_collected", 0),
                "max_sources": 10000,
                "sources_per_hour": metrics.get("sources_per_hour", 0)
            }

            acoes = self.engine.evaluate(contexto)

            # Se há ação "parar", para
            if any(a["acao"] == "parar" for a in acoes):
                print("Regra de parada acionada!")
                break

            # Continua
            sleep(60)
```

### Qualidade de Dados com RegrasEngine
```python
class QualityValidatorWithRegras:
    def __init__(self):
        self.engine = RegrasEngine()

    def validate(self, data, source_type):
        """Valida qualidade usando regras"""
        score = self.calculate_quality_score(data)

        # Avalia regras
        contexto = {
            "modulo": "rastreador",
            "data_id": data["id"],
            "quality_score": score
        }

        acoes = self.engine.evaluate(contexto)

        # Se há ação "rejeitar", rejeita
        if any(a["acao"] == "rejeitar" for a in acoes):
            return {
                "passed": False,
                "score": score,
                "reason": "quality_rule_failed"
            }

        # Passou
        return {"passed": True, "score": score}
```

---

## Comandos CLI

```bash
# Carregar regras
regras load

# Avaliar regras para um contexto
regras evaluate --modulo rastreador --context sources_collected=10000

# Recarregar regras
regras reload

# Ver histórico de decisões
regras history --rule-id R-OP-01 --limit 20

# Testar regra isoladamente
regras test --rule-id R-OP-01 --context sources_collected=10000

# Ver estatísticas de regras
regras stats

# Ver regras carregadas
regras list
```

---

## Roadmap

### v0.1 (MVP)
- [ ] RegrasEngine básico
- [ ] Loader de YAML
- [ ] Parser de condições simples
- [ ] Actions básicos (parar, rejeitar, retry)
- [ ] Logger de decisões

### v0.5
- [ ] Integração com todos os módulos
- [ ] Parser avançado (expressões complexas)
- [ ] Actions completos (todos do ecossistema + RAG)
- [ ] Dashboard de regras ativas
- [ ] Regras customizáveis por projeto

### v1.0
- [ ] Regras dinâmicas (adicionar em runtime)
- [ ] Versionamento de regras
- [ ] A/B testing de regras
- [ ] Auto-tuning de thresholds
- [ ] API REST para gerenciar regras

---

## Integração com 212 Regras

### Regras Carregadas Automaticamente
```python
# Ao inicializar
engine = RegrasEngine()

# Carrega automaticamente:
# - rules/ecossistema.yaml (100 regras)
# - rules/rag.yaml (112 regras)
# Total: 212 regras

print(f"Regras carregadas: {engine.count_rules()}")
# Saída: Regras carregadas: 212
```

### Categorização
```python
# Por categoria
engine.get_rules_by_category("operacao")     # 15 regras
engine.get_rules_by_category("qualidade")     # 20 regras
engine.get_rules_by_category("decisao")       # 15 regras
engine.get_rules_by_category("embeddings")    # 16 regras
engine.get_rules_by_category("busca")         # 20 regras
engine.get_rules_by_category("freshness")     # 14 regras
# ...

# Por módulo
engine.get_rules_by_module("rastreador")      # 9 regras
engine.get_rules_by_module("minerador")       # 6 regras
engine.get_rules_by_module("rag")             # 50 regras
# ...
```

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 19*
