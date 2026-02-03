"""
Health Check Engine — Motor de Health Checks

Versão: 1.0
Data: 2026-01-31
"""

import os
from typing import Dict, List, Any
from datetime import datetime
from abc import ABC, abstractmethod


class HealthChecker(ABC):
    """Classe abstrata para checkers de saúde"""

    @abstractmethod
    def check(self) -> Dict[str, Any]:
        """Executa check de saúde"""
        pass

    @abstractmethod
    def get_module_name(self) -> str:
        """Retorna nome do módulo"""
        pass


class BaseHealthChecker(HealthChecker):
    """Checker base para todos os módulos"""

    def __init__(self, module_name: str):
        """Inicializa checker base"""
        self.module_name = module_name

    def get_module_name(self) -> str:
        """Retorna nome do módulo"""
        return self.module_name

    def check(self) -> Dict[str, Any]:
        """Check base (sempre saudável)"""
        return {
            "status": "healthy",
            "module": self.module_name,
            "timestamp": datetime.now().isoformat(),
            "details": {}
        }

    def create_error(self, error: str) -> Dict[str, Any]:
        """Cria resultado de erro"""
        return {
            "status": "unhealthy",
            "module": self.module_name,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }

    def create_warning(self, warning: str) -> Dict[str, Any]:
        """Cria resultado de aviso (degraded)"""
        return {
            "status": "degraded",
            "module": self.module_name,
            "warning": warning,
            "timestamp": datetime.now().isoformat()
        }

    def create_success(self, details: Dict[str, Any] = None) -> Dict[str, Any]:
        """Cria resultado de sucesso"""
        return {
            "status": "healthy",
            "module": self.module_name,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
