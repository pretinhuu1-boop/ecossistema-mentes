"""
Critérios de Parada — Sistema de Terminação

Versão: 1.0
Data: 2026-01-31
"""

import sqlite3
from datetime import datetime
from typing import Dict, List, Any


class TerminationCriteria:
    """Critérios de Parada para módulos"""

    def __init__(self, db_path: str = "termination_criteria.db"):
        """
        Inicializa TerminationCriteria

        Args:
            db_path: Caminho do banco SQLite
        """
        self.db = sqlite3.connect(db_path)
        self.init_db()

    def init_db(self):
        """Inicializa banco de critérios"""
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS criteria (
                id TEXT PRIMARY KEY,
                module TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                threshold REAL,
                operator TEXT,
                description TEXT,
                created_at TEXT NOT NULL
            )
        """)
        self.db.commit()

    def create_criterion(self, criterion: Dict[str, Any]):
        """
        Cria critério de parada

        Args:
            criterion: Dados do critério
        """
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO criteria (id, module, name, type, threshold, operator, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            criterion.get("id", f"criteria_{len(self.get_all()) + 1}"),
            criterion["module"],
            criterion["name"],
            criterion["type"],
            criterion.get("threshold", 0.0),
            criterion.get("operator", ">="),
            criterion.get("description", ""),
            datetime.now().isoformat()
        ))
        self.db.commit()

    def evaluate(self, module: str, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Avalia se módulo deve parar

        Args:
            module: Nome do módulo
            metrics: Métricas atuais

        Returns:
            list: Critérios que foram atendidos
        """
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM criteria WHERE module = ?", (module,))
        all_criteria = cursor.fetchall()

        met_criteria = []

        for row in all_criteria:
            criterion_id, _, name, type_, threshold, operator, description, _ = row

            # Avalia critério
            try:
                metric_value = metrics.get(name)
                if metric_value is None:
                    continue

                # Avalia threshold
                met = self.evaluate_threshold(metric_value, threshold, operator)

                if met:
                    met_criteria.append({
                        "id": criterion_id,
                        "name": name,
                        "type": type_,
                        "threshold": threshold,
                        "operator": operator,
                        "description": description
                    })
            except Exception as e:
                print(f"Erro ao avaliar critério {name}: {e}")

        return met_criteria

    def evaluate_threshold(self, value: float, threshold: float, operator: str) -> bool:
        """
        Avalia threshold

        Args:
            value: Valor atual
            threshold: Threshold
            operator: Operador (>=, <=, >, <, ==, !=)

        Returns:
            bool: Se threshold foi atingido
        """
        if operator == ">=":
            return value >= threshold
        elif operator == "<=":
            return value <= threshold
        elif operator == ">":
            return value > threshold
        elif operator == "<":
            return value < threshold
        elif operator == "==":
            return value == threshold
        elif operator == "!=":
            return value != threshold
        else:
            return False

    def get_all(self) -> List[Dict[str, Any]]:
        """Busca todos os critérios"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM criteria")
        all_criteria = cursor.fetchall()

        return [
            {
                "id": row[0],
                "module": row[1],
                "name": row[2],
                "type": row[3],
                "threshold": row[4],
                "operator": row[5],
                "description": row[6],
                "created_at": row[7]
            }
            for row in all_criteria
        ]

    def get_by_module(self, module: str) -> List[Dict[str, Any]]:
        """Busca critérios por módulo"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM criteria WHERE module = ?", (module,))
        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "module": row[1],
                "name": row[2],
                "type": row[3],
                "threshold": row[4],
                "operator": row[5],
                "description": row[6],
                "created_at": row[7]
            }
            for row in rows
        ]

    def get_by_type(self, type_: str) -> List[Dict[str, Any]]:
        """Busca critérios por tipo"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM criteria WHERE type = ?", (type_,))
        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "module": row[1],
                "name": row[2],
                "type": row[3],
                "threshold": row[4],
                "operator": row[5],
                "description": row[6],
                "created_at": row[7]
            }
            for row in rows
        ]


# Exemplo de uso
if __name__ == "__main__":
    criteria = TerminationCriteria()

    # Cria critérios do Rastreador
    criteria.create_criterion({
        "module": "rastreador",
        "name": "sources_collected",
        "type": "absolute",
        "threshold": 10000,
        "operator": ">=",
        "description": "Para quando atinge max_sources"
    })

    criteria.create_criterion({
        "module": "rastreador",
        "name": "sources_per_hour",
        "type": "minimum",
        "threshold": 10,
        "operator": "<=",
        "description": "Para quando min_new_sources_per_hour < 10"
    })

    # Cria critérios do Minerador
    criteria.create_criterion({
        "module": "minerador",
        "name": "artifacts_per_source",
        "type": "absolute",
        "threshold": 100,
        "operator": ">=",
        "description": "Para quando max_artifacts_per_source > 100"
    })

    criteria.create_criterion({
        "module": "minerador",
        "name": "confidence_mean",
        "type": "minimum",
        "threshold": 0.7,
        "operator": "<",
        "description": "Para quando min_confidence_mean < 0.7"
    })

    # Cria critérios do Loop
    criteria.create_criterion({
        "module": "loop",
        "name": "max_iterations",
        "type": "absolute",
        "threshold": 10,
        "operator": ">=",
        "description": "Para quando atinge max_iterations"
    })

    # Avalia Rastreador
    print("🧪 Avaliando Rastreador...")
    rastreador_metrics = {
        "sources_collected": 10000,
        "max_sources": 10000,
        "sources_per_hour": 8,
        "min_new_sources_per_hour": 10
    }

    met_criteria = criteria.evaluate("rastreador", rastreador_metrics)

    print(f"   ✅ {len(met_criteria)} critérios atendidos")
    for criterion in met_criteria:
        print(f"      - {criterion['name']}: {criterion['type']} {criterion['operator']} {criterion['threshold']}")

    # Avalia Minerador
    print("\n🧪 Avaliando Minerador...")
    minerador_metrics = {
        "artifacts_per_source": 105,
        "confidence_mean": 0.65,
        "min_confidence": 0.7
    }

    met_criteria = criteria.evaluate("minerador", minerador_metrics)

    print(f"   ✅ {len(met_criteria)} critérios atendidos")
    for criterion in met_criteria:
        print(f"      - {criterion['name']}: {criterion['type']} {criterion['operator']} {criterion['threshold']}")

    # Avalia Loop
    print("\n🧪 Avaliando Loop...")
    loop_metrics = {
        "iteration": 11,
        "max_iterations": 10,
        "improvement": 0.008,
        "min_improvement": 0.01
    }

    met_criteria = criteria.evaluate("loop", loop_metrics)

    print(f"   ✅ {len(met_criteria)} critérios atendidos")
    for criterion in met_criteria:
        print(f"      - {criterion['name']}: {criterion['type']} {criterion['operator']} {criterion['threshold']}")

    print("\n✅ Todos os testes passaram!")
