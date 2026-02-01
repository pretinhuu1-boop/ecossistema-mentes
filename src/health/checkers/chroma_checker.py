import os
import chromadb
from datetime import datetime
from typing import Dict, Any
from .base import BaseHealthChecker

class ChromaHealthChecker(BaseHealthChecker):
    """Checker de saúde para o ChromaDB"""

    def __init__(self):
        super().__init__("chroma")
        self.db_path = os.getenv("CHROMA_DB_PATH", "./data/vector_store/chroma.db")

    def check(self) -> Dict[str, Any]:
        """Executa check no ChromaDB usando heartbeat()"""
        try:
            # Tenta conectar e pedir batimento
            client = chromadb.PersistentClient(path=self.db_path)
            heartbeat = client.heartbeat()
            
            if heartbeat:
                collections = client.list_collections()
                details = {
                    "heartbeat": heartbeat,
                    "collections_count": len(collections),
                    "db_path": self.db_path
                }
                return self.create_success(details)
            else:
                return self.create_error("ChromaDB heartbeat returned 0")
        except Exception as e:
            return self.create_error(str(e))
