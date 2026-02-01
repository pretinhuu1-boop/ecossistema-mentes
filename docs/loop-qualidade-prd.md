# LOOP DE QUALIDADE — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 3)

---

## Problema

**Hoje:**
- Loop avalia → Melhora → Repete
- **Mas MELHORAR COMO? O que exatamente ele faz?**

**Precisamos de:**
- Estratégias de melhoria específicas por métrica
- Sistema sabe exatamente O QUE fazer pra melhorar
- Priorização automática de estratégias

---

## Stack Técnica

### Motor (Python)
- **SQLite** — Estado salvo
- **Python** — Lógica de estratégias

### Integração
- **Orquestrador** → Coleta métricas → Aplica estratégias
- **Rastreador/Minerador** → Recebem instruções de melhoria

---

## Estratégias de Melhoria

### 1. Se COBERTURA baixa (< 95%)
```python
STRATEGIES_LOW_COVERAGE = [
    "expand_search_synonyms",          # Buscar sinônimos do tema
    "search_related_authors",            # Buscar autores relacionados
    "discover_hidden_sources",          # Descobrir fontes escondidas
    "check_source_list_completeness"   # Verificar se lista está completa
]
```

### 2. Se CONFIDENCE baixa (< 0.85)
```python
STRATEGIES_LOW_CONFIDENCE = [
    "refine_extraction_prompts",       # Refinar prompts de extração
    "cross_reference_sources",          # Cross-referenciar fontes
    "manual_review_flag",               # Pedir revisão manual
    "increase_context_windows"           # Aumentar janela de contexto
]
```

### 3. Se CONSISTÊNCIA baixa (< 90%)
```python
STRATEGIES_LOW_CONSISTENCY = [
    "investigate_contradictions",       # Investigar contradições
    "mark_temporal_versions",           # Marcar versões temporais
    "add_context_notes",                # Adicionar notas de contexto
    "separate_by_time_period"           # Separar por período
]
```

### 4. Se GAPS alto (> 3)
```python
STRATEGIES_HIGH_GAPS = [
    "identify_missing_themes",         # Identificar temas faltando
    "search_theme_specific",             # Buscar específico por tema
    "review_collection_strategy",       # Revisar estratégia de coleta
    "expand_source_diversity"           # Expandir diversidade de fontes
]
```

---

## Workflow de Melhoria

```
1. Avaliar métricas
   ↓
2. Verificar thresholds
   ↓
3. Identificar gaps (o que tá abaixo do threshold?)
   ↓
4. Selecionar estratégias (pra cada gap, selecionar estratégias)
   ↓
5. Priorizar estratégias (qual é mais urgente?)
   ↓
6. Executar estratégias (uma por uma ou em paralelo)
   ↓
7. Re-avaliar métricas
   ↓
8. Repetir se necessário
```

---

## Improver

```python
class QualityImprover:
    def __init__(self, project_name):
        self.project_name = project_name
        self.STRATEGIES = {
            "low_coverage": STRATEGIES_LOW_COVERAGE,
            "low_confidence": STRATEGIES_LOW_CONFIDENCE,
            "low_consistency": STRATEGIES_LOW_CONSISTENCY,
            "high_gaps": STRATEGIES_HIGH_GAPS
        }

    def improve(self, metrics, threshold_level):
        """Melhora qualidade baseada nas métricas"""

        # 1. Identificar gaps
        gaps = self.identify_gaps(metrics, threshold_level)

        if not gaps:
            return {"status": "no_gaps", "action": "done"}

        # 2. Selecionar estratégias
        strategies = self.select_strategies(gaps)

        # 3. Priorizar estratégias
        prioritized = self.prioritize_strategies(strategies, metrics)

        # 4. Executar estratégias
        results = []
        for strategy in prioritized:
            result = self.execute_strategy(strategy)
            results.append(result)

        return {
            "status": "improved",
            "gaps_found": gaps,
            "strategies_executed": len(results),
            "results": results
        }

    def identify_gaps(self, metrics, threshold_level):
        """Identifica o que tá abaixo do threshold"""
        thresholds = THRESHOLDS[threshold_level]
        gaps = []

        if metrics["cobertura"] < thresholds["cobertura"]:
            gaps.append("low_coverage")

        if metrics["confidence"] < thresholds["confidence"]:
            gaps.append("low_confidence")

        if metrics["consistencia"] < thresholds["consistencia"]:
            gaps.append("low_consistency")

        if metrics["gaps"] > thresholds["gaps"]:
            gaps.append("high_gaps")

        return gaps

    def select_strategies(self, gaps):
        """Seleciona estratégias pra cada gap"""
        strategies = []

        for gap in gaps:
            strategies.extend(self.STRATEGIES[gap])

        return strategies

    def prioritize_strategies(self, strategies, metrics):
        """Prioriza estratégias baseado em urgência"""
        # Urgência = impacto * facilidade
        prioritized = sorted(
            strategies,
            key=lambda s: self.urgency_score(s, metrics),
            reverse=True
        )
        return prioritized

    def urgency_score(self, strategy, metrics):
        """Calcula score de urgência de uma estratégia"""
        # Simulação: cada estratégia tem score fixo
        URGENCY_SCORES = {
            "expand_search_synonyms": 0.9,
            "refine_extraction_prompts": 0.8,
            "investigate_contradictions": 0.7,
            "identify_missing_themes": 0.85,
            # ... etc
        }

        return URGENCY_SCORES.get(strategy, 0.5)

    def execute_strategy(self, strategy):
        """Executa uma estratégia"""
        # Chama o módulo correspondente
        if strategy == "expand_search_synonyms":
            return Rastreador.expand_synonyms(self.project_name)
        elif strategy == "refine_extraction_prompts":
            return Minerador.refine_prompts(self.project_name)
        elif strategy == "investigate_contradictions":
            return Validator.investigate(self.project_name)
        # ... etc

        return {"strategy": strategy, "status": "executed"}
```

---

## Thresholds

```python
THRESHOLDS = {
    "mvp": {
        "cobertura": 0.75,
        "confidence": 0.70,
        "consistencia": 0.80,
        "gaps": 10
    },
    "producao": {
        "cobertura": 0.90,
        "confidence": 0.80,
        "consistencia": 0.85,
        "gaps": 5
    },
    "enterprise": {
        "cobertura": 0.95,
        "confidence": 0.85,
        "consistencia": 0.90,
        "gaps": 3
    }
}
```

---

## Integração com Orquestrador

### Loop de Qualidade Orquestrado
```python
@celery.task(name="loop.quality")
def execute_quality_loop(project_name, threshold_level):
    """Executa loop de qualidade via Orquestrador"""

    # 1. Avaliar métricas
    metrics = QualityEvaluator.evaluate(project_name)

    # 2. Publicar evento
    publish(EventType.QUALITY_EVALUATED, {
        "project_name": project_name,
        "metrics": metrics
    })

    # 3. Verificar thresholds
    thresholds = THRESHOLDS[threshold_level]

    if not atingiu_threshold(metrics, thresholds):
        # 4. Melhorar
        improver = QualityImprover(project_name)
        result = improver.improve(metrics, threshold_level)

        # 5. Repetir loop
        execute_quality_loop.delay(project_name, threshold_level)
    else:
        # 6. DONE
        publish(EventType.LOOP_COMPLETED, {
            "project_name": project_name,
            "status": "done"
        })
```

---

## Comandos CLI

```bash
# Executar loop de qualidade
loop execute --project alan_nicolas --threshold enterprise

# Ver estratégias disponíveis
loop strategies

# Ver gaps identificados
loop gaps --project alan_nicolas

# Ver priorização
loop prioritize --project alan_nicolas
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Estratégias básicas definidas
- [ ] Improver implementado
- [ ] Integração com Orquestrador

### v0.5
- [ ] Priorização dinâmica
- [ ] Score de urgência
- [ ] Paralelização de estratégias

### v1.0
- [ ] Aprendizado de quais estratégias funcionam melhor
- [ ] Auto-tuning de thresholds
- [ ] Feedback de estratégias

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 3*
