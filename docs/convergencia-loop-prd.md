# CONVERGÊNCIA DO LOOP — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 17)

---

## Problema

**Hoje:**
- Loop pode não convergir
- Pode rodar infinitamente
- Não há critérios de parada definitivos

**Precisamos de:**
- Verificação de convergência
- Critérios de parada definitivos
- Detecção de oscilação

---

## Stack Técnica

### Motor (Python)
- **Python** — Lógica de convergência
- **SQLite** — Histórico de iterações

### Integração
- **Loop de Qualidade** — Verifica convergência antes de cada iteração

---

## Funcionalidades

### Core
- [ ] Verificação de convergência
- [ ] Detecção de oscilação
- [ ] Critérios de parada
- [ ] Histórico de iterações

---

## Verificador de Convergência

```python
class ConvergenceChecker:
    def __init__(self, max_iterations=10, min_improvement=0.01):
        self.max_iterations = max_iterations
        self.min_improvement = min_improvement
        self.history = []

    def check_convergence(self, metrics):
        """
        Verifica se loop convergiu

        Args:
            metrics: Métricas atuais

        Returns:
            tuple: (converged, reason)
        """
        # 1. Adiciona ao histórico
        self.history.append(metrics)

        # 2. Se histórico é curto, ainda não convergiu
        if len(self.history) < 3:
            return False, "insufficient_history"

        # 3. Calcula melhoria nas últimas 2 iterações
        recent = self.history[-2:]
        improvements = self.calculate_improvements(recent)

        # 4. Se melhoria < threshold em todas, convergiu
        if all(imp < self.min_improvement for imp in improvements):
            return True, "converged_low_improvement"

        # 5. Se atingiu máximo de iterações, força parada
        if len(self.history) >= self.max_iterations:
            return True, "max_iterations_reached"

        # 6. Verifica se está oscilando
        if self.is_oscillating():
            return True, "oscillating"

        # 7. Continua
        return False, "not_converged"

    def calculate_improvements(self, metrics_list):
        """Calcula melhoria entre métricas"""
        improvements = []

        for i in range(1, len(metrics_list)):
            prev = metrics_list[i-1]
            curr = metrics_list[i]

            improvement = self.calculate_improvement(prev, curr)
            improvements.append(improvement)

        return improvements

    def calculate_improvement(self, prev_metrics, curr_metrics):
        """Calcula melhoria entre duas métricas"""
        # Melhoria = média das melhorias em cada métrica
        metric_improvements = []

        for key in prev_metrics:
            if key in curr_metrics and isinstance(prev_metrics[key], (int, float)):
                prev_val = prev_metrics[key]
                curr_val = curr_metrics[key]

                # Melhoria relativa
                if prev_val != 0:
                    improvement = abs((curr_val - prev_val) / prev_val)
                else:
                    improvement = 0.0

                metric_improvements.append(improvement)

        # Média
        if metric_improvements:
            return sum(metric_improvements) / len(metric_improvements)
        else:
            return 0.0

    def is_oscillating(self, window=5):
        """Verifica se está oscilando"""
        if len(self.history) < window * 2:
            return False

        # Pega últimas window*2 iterações
        recent = self.history[-(window*2):]

        # Divide em duas metades
        first_half = recent[:window]
        second_half = recent[window:]

        # Calcula média de cada metade
        first_avg = self.calculate_metrics_avg(first_half)
        second_avg = self.calculate_metrics_avg(second_half)

        # Se as médias são muito parecidas, está oscilando
        difference = abs(first_avg - second_avg)

        # Se diferença < 5%, oscilando
        return difference < 0.05

    def calculate_metrics_avg(self, metrics_list):
        """Calcula média das métricas"""
        if not metrics_list:
            return 0.0

        all_values = []
        for metrics in metrics_list:
            for key, val in metrics.items():
                if isinstance(val, (int, float)):
                    all_values.append(val)

        if not all_values:
            return 0.0

        return sum(all_values) / len(all_values)

    def reset(self):
        """Reseta histórico"""
        self.history = []
```

---

## Integração com Loop de Qualidade

```python
class QualityLoopWithConvergence:
    def __init__(self, project_name):
        self.project_name = project_name
        self.convergence = ConvergenceChecker(
            max_iterations=10,
            min_improvement=0.01
        )

    def execute(self):
        """Executa loop com verificação de convergência"""

        while True:
            # 1. Executa iteração
            metrics = self.execute_iteration()

            # 2. Verifica convergência
            converged, reason = self.convergence.check_convergence(metrics)

            # 3. Se convergiu, para
            if converged:
                print(f"✅ Loop convergiu: {reason}")
                print(f"Total de iterações: {len(self.convergence.history)}")
                break

            # 4. Continua
            print(f"🔄 Continuando... ({len(self.convergence.history)} iterações)")

    def execute_iteration(self):
        """Executa uma iteração do loop (stub)"""
        # TODO: Implementar execução real
        return {
            "cobertura": 0.95,
            "confidence": 0.86,
            "consistencia": 0.92,
            "gaps": 1
        }
```

---

## Comandos CLI

```bash
# Verificar convergência do loop
convergence check --project alan_nicolas

# Ver histórico de iterações
convergence history --project alan_nicolas

# Verificar se está oscilando
convergence is-oscillating --project alan_nicolas

# Resetar histórico de convergência
convergence reset --project alan_nicolas
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Verificação de convergência básica
- [ ] Detecção de oscilação
- [ ] Histórico de iterações

### v0.5
- [ ] Thresholds customizáveis
- [ ] Análise de tendências
- [ ] Predição de iterações restantes

### v1.0
- [ ] Auto-tuning de thresholds
- [ ] Detecção avançada de oscilação
- [ ] Integração com Critérios de Parada

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 17*
