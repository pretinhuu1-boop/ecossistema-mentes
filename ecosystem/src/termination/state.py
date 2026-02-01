"""
TerminationState — Estado de Terminação

Versão: 1.0
Data: 2026-01-31
"""

import sqlite3
from datetime import datetime
from typing import Dict, List, Any


class TerminationState:
    """Estado de Terminação (histórico de paradas)"""

    def __init__(self, db_path: str = "termination_state.db"):
        """
        Inicializa TerminationState

        Args:
            db_path: Caminho do banco SQLite
        """
        self.db = sqlite3.connect(db_path)
        self.init_db()

    def init_db(self):
        """Inicializa banco de estado de terminação"""
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS terminations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                criteria TEXT,
                metrics TEXT,
                reason TEXT
            )
        """)
        self.db.commit()

    def save_termination(self, module: str, criteria: List[Dict[str, Any]], metrics: Dict[str, Any], reason: str):
        """
        Salva estado de terminação

        Args:
            module: Nome do módulo
            criteria: Critérios atendidos
            metrics: Métricas atuais
            reason: Razão da parada
        """
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO terminations (module, timestamp, criteria, metrics, reason)
            VALUES (?, ?, ?, ?, ?)
        """, (
            module,
            datetime.now().isoformat(),
            str(criteria),
            str(metrics),
            reason
        ))
        self.db.commit()

    def get_history(self, module: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca histórico de paradas

        Args:
            module: Filtrar por módulo (opcional)
            limit: Número máximo de resultados

        Returns:
            list: Histórico de paradas
        """
        cursor = self.db.cursor()

        query = "SELECT * FROM terminations WHERE 1=1"
        params = []

        if module:
            query += " AND module = ?"
            params.append(module)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "module": row[1],
                "timestamp": row[2],
                "criteria": row[3],
                "metrics": row[4],
                "reason": row[5]
            }
            for row in rows
        ]

    def get_module_history(self, module: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Busca histórico de paradas de um módulo"""
        return self.get_history(module=module, limit=limit)

    def get_stats(self, days: int = 7) -> Dict[str, Any]:
        """
        Busca estatísticas de paradas

        Args:
            days: Número de dias

        Returns:
            dict: Estatísticas
        """
        cursor = self.db.cursor()

        # Total de paradas
        cursor.execute("SELECT COUNT(*) FROM terminations")
        total = cursor.fetchone()[0]

        # Paradas por módulo
        cursor.execute("""
            SELECT module, COUNT(*) as count
            FROM terminations
            GROUP BY module
            ORDER BY count DESC
        """)
        by_module = cursor.fetchall()

        # Paradas recentes
        cursor.execute("""
            SELECT * FROM terminations
            WHERE timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp DESC
            LIMIT 100
        """.format(days))
        recent = cursor.fetchall()

        return {
            "total": total,
            "by_module": by_module,
            "recent_count": len(recent),
            "recent": recent[:10]
        }


# Exemplo de uso
if __name__ == "__main__":
    state = TerminationState()

    # Exemplo: Salva parada do Rastreador
    criteria = [
        {"id": "R-OP-01", "name": "sources_collected", "threshold": 10000, "operator": ">="}
    ]

    metrics = {
        "sources_collected": 10000,
        "max_sources": 10000
    }

    reason = "Para quando atinge max_sources"

    state.save_termination("rastreador", criteria, metrics, reason)
    print("✅ Estado de terminação salvo!")

    # Exemplo: Busca histórico
    history = state.get_history(module="rastreador", limit=5)
    print(f"\n📋 Histórico do Rastreador: {len(history)} paradas")

    for term in history:
        print(f"  {term['timestamp']}: {term['reason']}")

    # Exemplo: Estatísticas
    stats = state.get_stats(days=7)
    print(f"\n📊 Estatísticas (últimos 7 dias):")
    print(f"  Total: {stats['total']}")
    print(f"  Por módulo:")
    for module, count in stats['by_module']:
        print(f"    - {module}: {count}")
