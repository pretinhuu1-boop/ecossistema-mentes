"""
RuleLogger — Histórico de decisões de regras

Versão: 1.0
Data: 2026-01-31
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple


class RuleLogger:
    """Histórico de decisões de regras"""

    def __init__(self, db_path: str = "rule_decisions.db"):
        """
        Inicializa RuleLogger

        Args:
            db_path: Caminho do banco SQLite (padrão: "rule_decisions.db")
        """
        self.db_path = db_path
        self.db = sqlite3.connect(self.db_path)
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
                resultado TEXT,
                prioridade TEXT
            )
        """)
        self.db.commit()

    def log(self, rule: Dict[str, Any], contexto: Dict[str, Any], resultado: Dict[str, Any]):
        """
        Logga decisão de regra

        Args:
            rule: Regra executada
            contexto: Contexto da decisão
            resultado: Resultado da ação
        """
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO decisions (timestamp, rule_id, rule_set, modulo, condicao,
                                   acao, contexto, resultado, prioridade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            rule.get("id", "unknown"),
            rule.get("rule_set", "unknown"),
            rule.get("modulo", "unknown"),
            rule.get("condicao", ""),
            rule.get("acao", "unknown"),
            json.dumps(contexto),
            json.dumps(resultado),
            rule.get("prioridade", "normal")
        ))
        self.db.commit()

    def get_history(self, rule_id: str = None, modulo: str = None, limit: int = 100) -> List[Tuple]:
        """
        Busca histórico de decisões

        Args:
            rule_id: Filtrar por rule_id (opcional)
            modulo: Filtrar por modulo (opcional)
            limit: Número máximo de resultados (padrão: 100)

        Returns:
            list: Histórico de decisões
        """
        cursor = self.db.cursor()

        query = "SELECT * FROM decisions WHERE 1=1"
        params = []

        if rule_id:
            query += " AND rule_id = ?"
            params.append(rule_id)

        if modulo:
            query += " AND modulo = ?"
            params.append(modulo)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        return cursor.fetchall()

    def get_rule_history(self, rule_id: str, limit: int = 20) -> List[Tuple]:
        """
        Busca histórico de uma regra específica

        Args:
            rule_id: ID da regra
            limit: Número máximo de resultados (padrão: 20)

        Returns:
            list: Histórico da regra
        """
        return self.get_history(rule_id=rule_id, limit=limit)

    def get_module_history(self, modulo: str, limit: int = 50) -> List[Tuple]:
        """
        Busca histórico de decisões de um módulo

        Args:
            modulo: Nome do módulo
            limit: Número máximo de resultados (padrão: 50)

        Returns:
            list: Histórico do módulo
        """
        return self.get_history(modulo=modulo, limit=limit)

    def get_stats(self, days: int = 7) -> Dict[str, Any]:
        """
        Busca estatísticas de decisões

        Args:
            days: Número de dias (padrão: 7)

        Returns:
            dict: Estatísticas
        """
        cursor = self.db.cursor()

        # Total de decisões
        cursor.execute("SELECT COUNT(*) FROM decisions")
        total = cursor.fetchone()[0]

        # Decisões por módulo
        cursor.execute("""
            SELECT modulo, COUNT(*) as count
            FROM decisions
            GROUP BY modulo
            ORDER BY count DESC
        """)
        by_module = cursor.fetchall()

        # Decisões por ação
        cursor.execute("""
            SELECT acao, COUNT(*) as count
            FROM decisions
            GROUP BY acao
            ORDER BY count DESC
        """)
        by_action = cursor.fetchall()

        # Decisões recentes
        cursor.execute("""
            SELECT * FROM decisions
            WHERE timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp DESC
            LIMIT 100
        """.format(days))
        recent = cursor.fetchall()

        return {
            "total": total,
            "by_module": by_module,
            "by_action": by_action,
            "recent_count": len(recent),
            "recent": recent[:10]
        }


# Exemplo de uso
if __name__ == "__main__":
    logger = RuleLogger()

    # Exemplo: Loggar uma decisão
    rule = {
        "id": "R-OP-01",
        "rule_set": "ecossistema",
        "modulo": "rastreador",
        "categoria": "operacao",
        "condicao": "sources_collected >= max_sources",
        "acao": "parar",
        "prioridade": "alta"
    }

    contexto = {
        "modulo": "rastreador",
        "metrics": {
            "sources_collected": 10000,
            "max_sources": 10000
        },
        "data_id": "source_001"
    }

    resultado = {
        "status": "stopped",
        "modulo": "rastreador"
    }

    logger.log(rule, contexto, resultado)
    print("✅ Decisão logada!")

    # Exemplo: Buscar histórico
    history = logger.get_rule_history("R-OP-01")
    print(f"\n📋 Histórico da regra R-OP-01: {len(history)} decisões")

    # Exemplo: Estatísticas
    stats = logger.get_stats(days=7)
    print(f"\n📊 Estatísticas (últimos 7 dias):")
    print(f"  Total: {stats['total']}")
    print(f"  Recentes: {stats['recent_count']}")
