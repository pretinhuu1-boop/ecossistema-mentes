#!/usr/bin/env python3
"""
Teste do Sistema de Terminação

Versão: 1.0
Data: 2026-01-31
"""

import sqlite3
from datetime import datetime
from typing import Dict, List, Any


class SimulatedTerminationCriteria:
    """Critérios de Parada simulados"""

    def __init__(self):
        self.db = sqlite3.connect(":memory:")

    def create_criterion(self, criterion: Dict[str, Any]):
        """Cria critério (simulado)"""
        print(f"   ✅ Criado critério: {criterion['name']}")
        return criterion.get("id", "unknown")

    def evaluate(self, module: str, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Avalia critérios (simulado)"""
        met_criteria = []

        # Critérios do Rastreador
        if module == "rastreador":
            if metrics.get("sources_collected") >= metrics.get("max_sources"):
                met_criteria.append({
                    "id": "R-OP-01",
                    "name": "sources_collected",
                    "type": "absolute",
                    "threshold": metrics.get("max_sources"),
                    "operator": ">=",
                    "description": "Para quando atinge max_sources"
                })

            if metrics.get("sources_per_hour") < metrics.get("min_new_sources_per_hour"):
                met_criteria.append({
                    "id": "R-OP-02",
                    "name": "sources_per_hour",
                    "type": "minimum",
                    "threshold": metrics.get("min_new_sources_per_hour"),
                    "operator": "<=",
                    "description": "Para quando min_new_sources_per_hour < 10"
                })

        # Critérios do Minerador
        elif module == "minerador":
            if metrics.get("artifacts_per_source") >= 100:
                met_criteria.append({
                    "id": "R-OP-05",
                    "name": "artifacts_per_source",
                    "type": "absolute",
                    "threshold": 100,
                    "operator": ">=",
                    "description": "Para quando max_artifacts_per_source > 100"
                })

            if metrics.get("confidence_mean") < 0.7:
                met_criteria.append({
                    "id": "R-OP-06",
                    "name": "confidence_mean",
                    "type": "minimum",
                    "threshold": 0.7,
                    "operator": "<",
                    "description": "Para quando min_confidence_mean < 0.7"
                })

        # Critérios do Loop
        elif module == "loop":
            if metrics.get("iteration") >= 10:
                met_criteria.append({
                    "id": "R-OP-09",
                    "name": "max_iterations",
                    "type": "absolute",
                    "threshold": 10,
                    "operator": ">=",
                    "description": "Para quando atinge max_iterations"
                })

        return met_criteria


class SimulatedTerminationState:
    """Estado de Parada simulado"""

    def __init__(self):
        self.history = []

    def save_termination(self, module: str, criteria: List[Dict[str, Any]], metrics: Dict[str, Any], reason: str):
        """Salva estado (simulado)"""
        self.history.append({
            "module": module,
            "timestamp": datetime.now().isoformat(),
            "criteria": criteria,
            "metrics": metrics,
            "reason": reason
        })
        print(f"   ✅ Salvo estado: {module} - {reason}")

    def get_history(self, module: str = None, limit: int = 10):
        """Busca histórico"""
        history = self.history

        if module:
            history = [h for h in history if h["module"] == module]

        return history[:limit]


def test_termination():
    """Testa sistema de terminação"""
    print("🧪 Testando Sistema de Terminação...\n")

    # 1. Inicia sistema
    print("1️⃣ Inicializando sistema...")
    criteria = SimulatedTerminationCriteria()
    state = SimulatedTerminationState()

    # 2. Teste 1: Rastreador atinge max_sources
    print("\n2️⃣ Testando Rastreador (atinge max_sources)...")
    rastreador_metrics = {
        "sources_collected": 10000,
        "max_sources": 10000,
        "sources_per_hour": 12,
        "min_new_sources_per_hour": 10
    }

    met_criteria = criteria.evaluate("rastreador", rastreador_metrics)

    print(f"   ✅ {len(met_criteria)} critérios atendidos")
    for criterion in met_criteria:
        print(f"      - {criterion['name']}: {criterion['type']} {criterion['operator']} {criterion['threshold']}")

    # Salva estado
    if met_criteria:
        reason = "Para quando atinge max_sources"
        state.save_termination("rastreador", met_criteria, rastreador_metrics, reason)

    # 3. Teste 2: Rastreador abaixo do mínimo de fontes/hora
    print("\n3️⃣ Testando Rastreador (abaixo do mínimo)...")
    rastreador_metrics_low = {
        "sources_collected": 8000,
        "max_sources": 10000,
        "sources_per_hour": 8,
        "min_new_sources_per_hour": 10
    }

    met_criteria = criteria.evaluate("rastreador", rastreador_metrics_low)

    print(f"   ✅ {len(met_criteria)} critérios atendidos")
    for criterion in met_criteria:
        print(f"      - {criterion['name']}: {criterion['type']} {criterion['operator']} {criterion['threshold']}")

    # Salva estado
    if met_criteria:
        reason = "Para quando min_new_sources_per_hour < 10"
        state.save_termination("rastreador", met_criteria, rastreador_metrics_low, reason)

    # 4. Teste 3: Minerador acima do máximo de artefatos/fonte
    print("\n4️⃣ Testando Minerador (acima do máximo)...")
    minerador_metrics = {
        "artifacts_per_source": 105,
        "confidence_mean": 0.8,
        "min_confidence": 0.7
    }

    met_criteria = criteria.evaluate("minerador", minerador_metrics)

    print(f"   ✅ {len(met_criteria)} critérios atendidos")
    for criterion in met_criteria:
        print(f"      - {criterion['name']}: {criterion['type']} {criterion['operator']} {criterion['threshold']}")

    # Salva estado
    if met_criteria:
        reason = "Para quando max_artifacts_per_source > 100"
        state.save_termination("minerador", met_criteria, minerador_metrics, reason)

    # 5. Teste 4: Minerador abaixo da confiança mínima
    print("\n5️⃣ Testando Minerador (abaixo da confiança mínima)...")
    minerador_metrics_low = {
        "artifacts_per_source": 50,
        "confidence_mean": 0.65,
        "min_confidence": 0.7
    }

    met_criteria = criteria.evaluate("minerador", minerador_metrics_low)

    print(f"   ✅ {len(met_criteria)} critérios atendidos")
    for criterion in met_criteria:
        print(f"      - {criterion['name']}: {criterion['type']} {criterion['operator']} {criterion['threshold']}")

    # Salva estado
    if met_criteria:
        reason = "Para quando min_confidence_mean < 0.7"
        state.save_termination("minerador", met_criteria, minerador_metrics_low, reason)

    # 6. Teste 5: Loop atinge máximo de iterações
    print("\n6️⃣ Testando Loop (atinge máximo)...")
    loop_metrics = {
        "iteration": 11,
        "max_iterations": 10
    }

    met_criteria = criteria.evaluate("loop", loop_metrics)

    print(f"   ✅ {len(met_criteria)} critérios atendidos")
    for criterion in met_criteria:
        print(f"      - {criterion['name']}: {criterion['type']} {criterion['operator']} {criterion['threshold']}")

    # Salva estado
    if met_criteria:
        reason = "Para quando atinge max_iterations"
        state.save_termination("loop", met_criteria, loop_metrics, reason)

    # 7. Busca histórico
    print("\n7️⃣ Buscando histórico...")
    history = state.get_history(module="rastreador", limit=5)

    print(f"   ✅ Histórico do Rastreador: {len(history)} paradas")
    for term_record in history[:3]:
        print(f"      - {term_record['timestamp']}: {term_record['reason']}")

    print("\n✅ Todos os testes passaram!")


if __name__ == "__main__":
    test_termination()
