import os
from datetime import datetime
from typing import Dict, Any
from .base import BaseHealthChecker

class ModuleHealthChecker(BaseHealthChecker):
    """Checker genérico para módulos internos (Rastreador, Minerador, Orquestrador)"""

    def __init__(self, module_name: str, logs_path: str):
        super().__init__(module_name)
        self.logs_path = logs_path

    def check(self) -> Dict[str, Any]:
        """Executa check verificando integridade básica (logs e diretórios)"""
        try:
            if not os.path.exists(self.logs_path):
                return self.create_warning(f"Log directory not found: {self.logs_path}")
            
            # Verifica se houve atividade de log nas últimas 24h (opcional)
            details = {
                "logs_path": self.logs_path,
                "status": "active"
            }
            return self.create_success(details)
        except Exception as e:
            return self.create_error(str(e))

class RastreadorHealthChecker(ModuleHealthChecker):
    def __init__(self):
        super().__init__("rastreador", "./logs/rastreador.log")

class MineradorHealthChecker(ModuleHealthChecker):
    def __init__(self):
        super().__init__("minerador", "./logs/minerador.log")

class OrquestradorHealthChecker(ModuleHealthChecker):
    def __init__(self):
        super().__init__("orquestrador", "./src/orquestrador") # Orquestrador checa o diretório de tasks
