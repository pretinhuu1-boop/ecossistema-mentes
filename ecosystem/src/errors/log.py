import sqlite3
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

class ErrorLog:
    """Persistência de erros em SQLite para auditoria e recovery."""
    
    def __init__(self, db_path: str = "error_log.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    error_type TEXT NOT NULL,
                    error_message TEXT NOT NULL,
                    error_traceback TEXT,
                    module TEXT,
                    function TEXT,
                    context TEXT,
                    handled_by TEXT
                )
            """)
            conn.commit()

    def log(self, error: Exception, error_type: str, context: Dict[str, Any]):
        """Registra uma ocorrência de erro."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO errors (timestamp, error_type, error_message, error_traceback, 
                                   module, function, context, handled_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                error_type,
                str(error),
                traceback.format_exc(),
                context.get("module"),
                context.get("function"),
                json.dumps(context),
                "RobustErrorHandler"
            ))
            conn.commit()

    def get_recent(self, limit: int = 50):
        """Retorna erros recentes."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM errors ORDER BY timestamp DESC LIMIT ?", (limit,))
            return cursor.fetchall()
