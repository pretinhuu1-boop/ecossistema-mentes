"""
Termination — Sistema de Critérios de Parada

Versão: 1.0
Data: 2026-01-31
"""

from typing import Dict, List, Any

from .criteria import TerminationCriteria
from .state import TerminationState


class Termination:
    """Sistema de Critérios de Parada"""

    def __init__(self, db_path: str = "termination.db"):
        """
        Inicializa Termination

        Args:
            db_path: Caminho do banco SQLite
        """
        self.criteria = TerminationCriteria(db_path)
        self.state = TerminationState(db_path)

    def evaluate(self, module: str, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Avalia se módulo deve parar

        Args:
            module: Nome do módulo
            metrics: Métricas atuais

        Returns:
            list: Critérios que foram atendidos (razão de parada)
        """
        print(f"🏁 Avaliando critérios de parada para {module}...")

        # Avalia critérios
        met_criteria = self.criteria.evaluate(module, metrics)

        if met_criteria:
            # Salva estado de terminação
            reason = f"Módulo {module} deve parar"
            self.state.save_termination(
                module,
                met_criteria,
                metrics,
                reason
            )

            print(f"✅ {len(met_criteria)} critérios atendidos")
            for criterion in met_criteria:
                print(f"      - {criterion['name']}: {criterion['type']} {criterion['operator']} {criterion['threshold']}")
        else:
            print("✅ Nenhum critério atendido")

        return met_criteria

    def should_stop(self, module: str, metrics: Dict[str, Any]) -> bool:
        """
        Verifica se módulo deve parar

        Args:
            module: Nome do módulo
            metrics: Métricas atuais

        Returns:
            bool: True se deve parar, False caso contrário
        """
        met_criteria = self.evaluate(module, metrics)
        return len(met_criteria) > 0

    def get_history(self, module: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Busca histórico de paradas"""
        return self.state.get_history(module=module, limit=limit)

    def get_stats(self, days: int = 7) -> Dict[str, Any]:
        """Busca estatísticas de paradas"""
        return self.state.get_stats(days=days)


# Exemplo de uso
if __name__ == "__main__":
    termination = Termination()

    # Exemplo 1: Rastreador atinge max_sources
    print("🧪 Exemplo 1: Rastreador atinge max_sources")
    rastreador_metrics = {
        "sources_collected": 10000,
        "max_sources": 10000
    }

    met_criteria = termination.evaluate("rastreador", rastreador_metrics)
    print(f"   Deve parar: {len(met_criteria) > 0}")

    # Exemplo 2: Minerador atinge min_confidence
    print("\n🧪 Exemplo 2: Minerador atinge min_confidence")
    minerador_metrics = {
        "confidence_mean": 0.65,
        "min_confidence": 0.7
    }

    met_criteria = termination.evaluate("minerador", minerador_metrics)
    print(f"   Deve parar: {len(met_criteria) > 0}")

    # Exemplo 3: Loop atinge max_iterations
    print("\n🧪 Exemplo 3: Loop atinge max_iterations")
    loop_metrics = {
        "iteration": 11,
        "max_iterations": 10
    }

    met_criteria = termination.evaluate("loop", loop_metrics)
    print(f"   Deve parar: {len(met_criteria) > 0}")
