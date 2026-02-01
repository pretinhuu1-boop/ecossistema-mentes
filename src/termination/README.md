# Critérios de Parada — Sistema de Terminação

**Versão:** 1.0
**Data:** 2026-01-31

---

## Visão Geral

Sistema de Critérios de Parada define quando cada módulo deve parar, com critérios claros e mensuráveis.

### Módulos

- **criteria.py** — TerminationCriteria (classe principal)
- **state.py** — TerminationState (histórico de paradas)
- **__init__.py** — Sistema de terminação

---

## Funcionalidades

### Core
- ✅ Define critérios de parada (thresholds)
- ✅ Avalia se módulo deve parar
- ✅ Suporta múltiplos tipos de critérios (absolute, minimum, maximum)
- ✅ Histórico de paradas (SQLite)
- ✅ Estatísticas de paradas

### Tipos de Critérios

- **absolute** — Para quando atinge valor absoluto (>=, <=)
- **minimum** — Para quando está abaixo do mínimo
- **maximum** — Para quando está acima do máximo
- **relative** — Para quando variação é > X%

---

## Uso Básico

```python
from termination import Termination

# Inicia sistema
term = Termination()

# Avalia Rastreador
rastreador_metrics = {
    "sources_collected": 10000,
    "max_sources": 10000
}

met_criteria = term.evaluate("rastreador", rastreador_metrics)
print(f"Deve parar: {len(met_criteria) > 0}")

# Verifica se deve parar
should_stop = term.should_stop("rastreador", rastreador_metrics)
print(f"Deve parar: {should_stop}")
```

---

## CLI

```bash
# Criar critério
termination create --module rastreador --name sources_collected --type absolute --threshold 10000 --operator ">=" --description "Para quando atinge max_sources"

# Avaliar módulo
termination evaluate --module rastreador --context sources_collected=10000,max_sources=10000

# Verificar se deve parar
termination should-stop --module rastreador --context sources_collected=10000,max_sources=10000

# Ver histórico
termination history --module rastreador --limit 10

# Ver estatísticas
termination stats
```

---

## Roadmap

### v0.1 (MVP) — EM PROGRESSO
- [x] Estrutura de diretórios
- [x] TerminationCriteria
- [x] TerminationState
- [ ] Testes

### v0.5
- [ ] CLI completa
- [ ] Integração com Rastreador
- [ ] Integração com Minerador
- [ ] Integração com Loop

### v1.0
- [ ] Critérios relativos
- [ ] Auto-tuning de thresholds
- [ ] Dashboard de paradas
