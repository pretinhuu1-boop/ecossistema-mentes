# CRITÉRIOS DE PARADA — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 11)

---

## Problema

**Hoje:**
- Nenhum módulo tem critérios de parada claros
- Pode rodar infinitamente
- Não sabe quando "terminou"

**Precisamos de:**
- Critérios de parada explícitos por módulo
- Sistema sabe exatamente quando parar
- Evita rodar desnecessariamente

---

## Stack Técnica

### Motor (Python)
- **Python** — Lógica de critérios
- **SQLite** — Estado de parada

### Integração
- **Todos os módulos** — Consultam critérios antes de continuar
- **Orquestrador** — Coordena parada

---

## Funcionalidades

### Core
- [ ] Critérios de parada por módulo
- [ ] Sistema sabe exatamente quando parar
- [ ] Logging de decisões de parada
- [ ] Configurável por projeto

### Critérios por Módulo

#### Rastreador
- `max_sources` — Máximo de fontes
- `min_new_sources_per_hour` — Se < X por hora, para
- `max_hours_without_new` — Se X horas sem novas, para
- `completeness_threshold` — Se X% de completude, para

#### Minerador
- `max_artifacts_per_source` — Máximo por fonte
- `min_confidence_mean` — Se média < X, para
- `max_hours_without_new` — Se X horas sem novos, para
- `saturation_threshold` — Se X% de saturação, para

#### Loop
- `max_iterations` — Máximo de iterações
- `min_improvement_per_iteration` — Se melhoria < X%, para
- `max_hours_without_improvement` — Se X horas sem melhoria, para

---

## Critérios de Parada

```python
class TerminationCriteria:
    def __init__(self, project_name):
        self.project_name = project_name
        self.state = TerminationState(project_name)

        # Critérios padrão
        self.DEFAULT_CRITERIA = {
            "rastreador": {
                "max_sources": 10000,
                "min_new_sources_per_hour": 10,
                "max_hours_without_new": 4,
                "completeness_threshold": 0.95
            },
            "minerador": {
                "max_artifacts_per_source": 100,
                "min_confidence_mean": 0.7,
                "max_hours_without_new": 2,
                "saturation_threshold": 0.9
            },
            "loop": {
                "max_iterations": 10,
                "min_improvement_per_iteration": 0.01,
                "max_hours_without_improvement": 6
            }
        }

    def should_stop(self, module, metrics):
        """
        Verifica se módulo deve parar

        Args:
            module: Nome do módulo ("rastreador", "minerador", "loop")
            metrics: Métricas atuais do módulo

        Returns:
            tuple: (should_stop: bool, reason: str)
        """
        # Busca critérios do módulo
        criteria = self.get_criteria(module)

        # Verifica cada critério
        reasons = []

        for criterion_name, threshold in criteria.items():
            if self.check_criterion(criterion_name, threshold, metrics):
                reasons.append({
                    "criterion": criterion_name,
                    "threshold": threshold,
                    "current_value": metrics.get(criterion_name),
                    "passed": True
                })

        # Se algum critério passou, para
        if reasons:
            # Registra parada
            self.state.log_stop(module, reasons)

            return True, f"Parada por: {', '.join([r['criterion'] for r in reasons])}"

        # Continua
        return False, "Continuando"

    def check_criterion(self, criterion_name, threshold, metrics):
        """Verifica se critério foi atingido"""

        CHECKS = {
            "max_sources": lambda: metrics.get("sources_collected", 0) >= threshold,
            "min_new_sources_per_hour": lambda: metrics.get("sources_per_hour", 0) < threshold,
            "max_hours_without_new": lambda: metrics.get("hours_without_new", 0) >= threshold,
            "completeness_threshold": lambda: metrics.get("completeness", 0) >= threshold,

            "max_artifacts_per_source": lambda: metrics.get("artifacts_per_source", 0) >= threshold,
            "min_confidence_mean": lambda: metrics.get("confidence_mean", 0) < threshold,
            "max_hours_without_new": lambda: metrics.get("hours_without_new", 0) >= threshold,
            "saturation_threshold": lambda: metrics.get("saturation", 0) >= threshold,

            "max_iterations": lambda: metrics.get("iteration", 0) >= threshold,
            "min_improvement_per_iteration": lambda: metrics.get("improvement", 0) < threshold,
            "max_hours_without_improvement": lambda: metrics.get("hours_without_improvement", 0) >= threshold
        }

        check = CHECKS.get(criterion_name, lambda: False)
        return check()

    def get_criteria(self, module):
        """Busca critérios do módulo (com override por projeto)"""
        # Busca critérios personalizados do projeto
        project_criteria = self.state.get_project_criteria(self.project_name, module)

        # Se não há, usa padrão
        if not project_criteria:
            return self.DEFAULT_CRITERIA.get(module, {})

        # Mescla padrão com personalizado (personalizado tem precedência)
        criteria = self.DEFAULT_CRITERIA.get(module, {}).copy()
        criteria.update(project_criteria)

        return criteria
```

---

## Estado de Parada

```python
class TerminationState:
    def __init__(self, project_name):
        self.project_name = project_name
        self.db = sqlite3.connect('termination_state.db')
        self.init_db()

    def init_db(self):
        """Inicializa banco"""
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                module TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                reasons TEXT NOT NULL,
                metrics TEXT
            )
        """)
        self.db.commit()

    def log_stop(self, module, reasons, metrics=None):
        """Registra parada"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO stops (project_name, module, timestamp, reasons, metrics)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.project_name,
            module,
            datetime.now().isoformat(),
            json.dumps(reasons),
            json.dumps(metrics) if metrics else None
        ))
        self.db.commit()

    def get_project_criteria(self, project_name, module):
        """Busca critérios personalizados do projeto"""
        # TODO: Implementar armazenamento de critérios personalizados
        return {}

    def get_stop_history(self, module=None, limit=10):
        """Busca histórico de paradas"""
        cursor = self.db.cursor()

        query = "SELECT * FROM stops WHERE project_name = ?"
        params = [self.project_name]

        if module:
            query += " AND module = ?"
            params.append(module)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        return cursor.fetchall()
```

---

## Integração com Módulos

### Rastreador com Critérios
```python
class RastreadorWithTermination:
    def __init__(self, project_name):
        self.project_name = project_name
        self.termination = TerminationCriteria(project_name)

    def collect_loop(self):
        """Loop de coleta com critérios de parada"""
        while True:
            # Coleta fontes
            new_sources = self.collect_batch()

            # Atualiza métricas
            metrics = self.get_metrics()

            # Verifica critérios de parada
            should_stop, reason = self.termination.should_stop("rastreador", metrics)

            if should_stop:
                print(f"Parando Rastreador: {reason}")
                break

            # Continua
            print(f"Continuando: {metrics['sources_collected']} fontes coletadas")
            sleep(60)  # Espera 1 minuto
```

### Loop de Qualidade com Critérios
```python
class QualityLoopWithTermination:
    def __init__(self, project_name):
        self.project_name = project_name
        self.termination = TerminationCriteria(project_name)

    def execute(self):
        """Executa loop com critérios de parada"""
        iteration = 0

        while True:
            iteration += 1

            # Executa iteração
            metrics = self.execute_iteration(iteration)

            # Verifica critérios de parada
            should_stop, reason = self.termination.should_stop("loop", metrics)

            if should_stop:
                print(f"Parando Loop (iteração {iteration}): {reason}")
                break

            # Continua
            print(f"Iteração {iteration}: Continuando...")
```

---

## Comandos CLI

```bash
# Ver critérios de parada
termination criteria --module rastreador --project alan_nicolas

# Definir critério personalizado
termination set --project alan_nicolas --module rastreador --criterion max_sources --value 5000

# Ver histórico de paradas
termination history --project alan_nicolas --module rastreador

# Verificar se deve parar agora
termination check --module rastreador --project alan_nicolas
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Critérios básicos por módulo
- [ ] Verificação de parada
- [ ] Logging de decisões

### v0.5
- [ ] Critérios personalizáveis por projeto
- [ ] Histórico de paradas
- [ ] Dashboard de critérios

### v1.0
- [ ] Auto-tuning de critérios (aprende o melhor valor)
- [ ] Predição de quando vai parar
- [ ] Alertas quando approaching thresholds

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 11*
