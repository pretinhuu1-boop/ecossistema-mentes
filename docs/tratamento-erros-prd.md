# TRATAMENTO DE ERROS ROBUSTO — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 12)

---

## Problema

**Hoje:**
- Erros podem falhar silenciosamente
- Não há recovery automático
- Não há retry inteligente

**Precisamos de:**
- Tratamento de erros robusto
- Recovery automático
- Retry inteligente com backoff

---

## Stack Técnica

### Motor (Python)
- **Python** — Lógica de erros
- **tenacity** — Retry com backoff
- **SQLite** — Log de erros

### Integração
- **Todos os módulos** — Usam handler de erros
- **Orquestrador** — Coordena recovery

---

## Funcionalidades

### Core
- [ ] Classificação de erros (transient, permanent, rate_limit)
- [ ] Retry inteligente com backoff exponencial
- [ ] Recovery automático
- [ ] Alertas para erros permanentes

### Estratégias por Tipo
- **Transient** — Retry com backoff
- **Permanent** — Não retry, alerta
- **Rate Limit** — Espera e retry

---

## Classificação de Erros

```python
class ErrorType(Enum):
    TRANSIENT = "transient"
    PERMANENT = "permanent"
    RATE_LIMIT = "rate_limit"
    UNKNOWN = "unknown"


class ErrorClassifier:
    def classify(self, error):
        """Classifica tipo de erro"""

        # Timeout → Transient
        if isinstance(error, (TimeoutError, ReadTimeoutError)):
            return ErrorType.TRANSIENT

        # Rate limit → Rate limit
        elif isinstance(error, (RateLimitError, TooManyRequests)):
            return ErrorType.RATE_LIMIT

        # Not found → Permanent
        elif isinstance(error, (NotFoundError, KeyError)):
            return ErrorType.PERMANENT

        # HTTP 4xx → Permanent
        elif hasattr(error, 'response') and hasattr(error.response, 'status_code'):
            if 400 <= error.response.status_code < 500:
                return ErrorType.PERMANENT
            elif 500 <= error.response.status_code < 600:
                return ErrorType.TRANSIENT

        # Unknown
        return ErrorType.UNKNOWN
```

---

## Handler de Erros

```python
class RobustErrorHandler:
    def __init__(self):
        self.classifier = ErrorClassifier()
        self.backoff = ExponentialBackoff()
        self.error_log = ErrorLog()
        self.alert = AlertManager()

    def handle(self, error, context):
        """
        Trata erro com estratégias robustas

        Args:
            error: Exceção capturada
            context: Contexto do erro (módulo, função, params, etc.)

        Returns:
            dict: Resultado do tratamento
        """
        # 1. Classifica erro
        error_type = self.classifier.classify(error)

        # 2. Registra erro
        self.error_log.log(error, error_type, context)

        # 3. Aplica estratégia
        if error_type == ErrorType.TRANSIENT:
            return self.handle_transient(error, context)

        elif error_type == ErrorType.RATE_LIMIT:
            return self.handle_rate_limit(error, context)

        elif error_type == ErrorType.PERMANENT:
            return self.handle_permanent(error, context)

        else:
            return self.handle_unknown(error, context)

    def handle_transient(self, error, context):
        """Trata erro transitório → Retry com backoff"""
        retry_count = context.get("retry_count", 0)
        max_retries = 3

        if retry_count >= max_retries:
            # Excedeu máximo → Aborta
            self.alert.send({
                "type": "max_retries_exceeded",
                "error": str(error),
                "context": context,
                "urgency": "critical"
            })
            return {"action": "abort", "reason": "max_retries_exceeded"}

        # Calcula tempo de espera (backoff exponencial)
        wait_time = self.backoff.calculate(retry_count)

        # Log
        print(f"Erro transitório: {error}")
        print(f"Esperando {wait_time}s antes de retry...")

        # Espera
        sleep(wait_time)

        # Retorna instruções de retry
        return {
            "action": "retry",
            "wait_time": wait_time,
            "new_context": {
                **context,
                "retry_count": retry_count + 1
            }
        }

    def handle_rate_limit(self, error, context):
        """Trata erro de rate limit → Espera e retry"""
        retry_count = context.get("retry_count", 0)
        max_retries = 5

        if retry_count >= max_retries:
            self.alert.send({
                "type": "max_retries_exceeded",
                "error": str(error),
                "context": context,
                "urgency": "critical"
            })
            return {"action": "abort", "reason": "max_retries_exceeded"}

        # Extrai tempo de espera do erro (se disponível)
        wait_time = None
        if hasattr(error, 'retry_after'):
            wait_time = error.retry_after
        elif hasattr(error, 'response') and 'Retry-After' in error.response.headers:
            wait_time = int(error.response.headers['Retry-After'])

        # Se não, usa backoff
        if wait_time is None:
            wait_time = self.backoff.calculate(retry_count)

        # Log
        print(f"Rate limit atingido: {error}")
        print(f"Esperando {wait_time}s...")

        # Espera
        sleep(wait_time)

        return {
            "action": "retry",
            "wait_time": wait_time,
            "new_context": {
                **context,
                "retry_count": retry_count + 1
            }
        }

    def handle_permanent(self, error, context):
        """Trata erro permanente → Não retry, alerta"""
        # Log
        print(f"Erro permanente: {error}")

        # Alerta
        self.alert.send({
            "type": "permanent_error",
            "error": str(error),
            "context": context,
            "urgency": "warning"
        })

        # Não retry
        return {
            "action": "abort",
            "reason": "permanent_error"
        }

    def handle_unknown(self, error, context):
        """Trata erro desconhecido → Alerta e aborta"""
        # Log
        print(f"Erro desconhecido: {error}")

        # Alerta
        self.alert.send({
            "type": "unknown_error",
            "error": str(error),
            "context": context,
            "urgency": "critical"
        })

        # Aborta
        return {
            "action": "abort",
            "reason": "unknown_error"
        }
```

---

## Backoff Exponencial

```python
class ExponentialBackoff:
    def __init__(self, base=1, max_wait=60):
        self.base = base  # Tempo base em segundos
        self.max_wait = max_wait  # Tempo máximo em segundos

    def calculate(self, retry_count):
        """
        Calcula tempo de espera com backoff exponencial

        Args:
            retry_count: Número de retentativas

        Returns:
            float: Tempo de espera em segundos
        """
        # Backoff exponencial com jitter
        wait_time = min(self.base * (2 ** retry_count), self.max_wait)

        # Adiciona jitter (aleatório entre 0-10%)
        jitter = wait_time * 0.1 * random.random()
        wait_time += jitter

        return wait_time
```

---

## Log de Erros

```python
class ErrorLog:
    def __init__(self):
        self.db = sqlite3.connect('error_log.db')
        self.init_db()

    def init_db(self):
        """Inicializa banco"""
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                error_type TEXT NOT NULL,
                error_message TEXT NOT NULL,
                error_traceback TEXT,
                module TEXT NOT NULL,
                function TEXT,
                context TEXT,
                handled_by TEXT
            )
        """)
        self.db.commit()

    def log(self, error, error_type, context):
        """Registra erro"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO errors (timestamp, error_type, error_message, error_traceback,
                               module, function, context, handled_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            error_type.value,
            str(error),
            traceback.format_exc(),
            context.get("module"),
            context.get("function"),
            json.dumps(context),
            "RobustErrorHandler"
        ))
        self.db.commit()

    def get_errors(self, module=None, error_type=None, limit=100):
        """Busca erros"""
        cursor = self.db.cursor()

        query = "SELECT * FROM errors WHERE 1=1"
        params = []

        if module:
            query += " AND module = ?"
            params.append(module)

        if error_type:
            query += " AND error_type = ?"
            params.append(error_type)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        return cursor.fetchall()
```

---

## Integração com Módulos

### Wrapper Decorator
```python
def robust_retry(max_retries=3):
    """Decorator para retry robusto"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = RobustErrorHandler()

            # Contexto
            context = {
                "module": func.__module__,
                "function": func.__name__,
                "args": args,
                "kwargs": kwargs,
                "retry_count": 0
            }

            while True:
                try:
                    # Executa função
                    return func(*args, **kwargs)

                except Exception as e:
                    # Trata erro
                    result = handler.handle(e, context)

                    if result["action"] == "retry":
                        # Atualiza contexto e retry
                        context = result["new_context"]
                        continue

                    elif result["action"] == "abort":
                        # Aborta
                        raise

        return wrapper
    return decorator


# Uso
@robust_retry(max_retries=3)
def scrape_source(source_id):
    """Scrapia fonte com retry robusto"""
    # ... código ...
    pass
```

---

## Comandos CLI

```bash
# Ver erros recentes
errors recent --limit 50

# Ver erros de um módulo
errors module --module rastreador

# Ver erros por tipo
errors type --type transient

# Ver estatísticas de erros
errors stats
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Classificação de erros básica
- [ ] Retry com backoff exponencial
- [ ] Log de erros

### v0.5
- [ ] Recovery automático
- [ ] Alertas por tipo de erro
- [ ] Dashboard de erros

### v1.0
- [ ] Auto-tuning de retry count
- [ ] Predição de falhas
- [ ] Integração com Health Checks

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 12*
