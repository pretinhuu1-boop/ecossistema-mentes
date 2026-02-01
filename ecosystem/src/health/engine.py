"""
Health Check Engine — Motor de Health Checks

Versão: 1.0
Data: 2026-01-31
"""

import os
from typing import Dict, List, Any
from datetime import datetime

from .checkers.base import BaseHealthChecker
from .checkers.redis_checker import RedisHealthChecker
from .checkers.celery_checker import CeleryHealthChecker
from .checkers.chroma_checker import ChromaHealthChecker
from .checkers.module_checkers import (
    RastreadorHealthChecker,
    MineradorHealthChecker,
    OrquestradorHealthChecker
)


class HealthCheckEngine:
    """Motor de Health Checks"""

    def __init__(self, checkers_dir: str = "checkers"):
        """
        Inicializa HealthCheckEngine

        Args:
            checkers_dir: Diretório dos checkers (padrão: "checkers")
        """
        self.checkers_dir = checkers_dir
        self.checkers = {}

        # Carrega checkers
        self.load_checkers()

    def load_checkers(self):
        """Carrega todos os checkers do diretório"""
        print("📥 Carregando health checkers...")

        # Checker Redis
        self.checkers["redis"] = RedisHealthChecker()

        # Checker Celery
        self.checkers["celery"] = CeleryHealthChecker()

        # Checker ChromaDB
        self.checkers["chroma"] = ChromaHealthChecker()

        # Checker Rastreador
        self.checkers["rastreador"] = RastreadorHealthChecker()

        # Checker Minerador
        self.checkers["minerador"] = MineradorHealthChecker()

        # Checker Orquestrador
        self.checkers["orquestrador"] = OrquestradorHealthChecker()

        total = len(self.checkers)
        print(f"✅ Carregados {total} health checkers")

    def check_all(self) -> Dict[str, Any]:
        """
        Executa check de saúde de todos os checkers

        Returns:
            dict: Status geral
        """
        print("🏥 Executando health checks de todos os módulos...")

        results = {}

        # Check cada módulo
        for module_name, checker in self.checkers.items():
            try:
                result = checker.check()
                results[module_name] = result
                print(f"✅ {module_name}: {result.get('status', 'unknown')}")
            except Exception as e:
                print(f"❌ {module_name}: Erro ao fazer check - {e}")
                results[module_name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }

        # Calcula status geral
        overall_status = self.calculate_overall_status(results)

        print(f"🎯 Status geral: {overall_status}")

        return {
            "overall_status": overall_status,
            "modules": results,
            "timestamp": datetime.now().isoformat()
        }

    def check_module(self, module_name: str) -> Dict[str, Any]:
        """
        Executa check de saúde de um módulo específico

        Args:
            module_name: Nome do módulo (redis, celery, chroma, etc.)

        Returns:
            dict: Status do módulo
        """
        checker = self.checkers.get(module_name)

        if not checker:
            return {
                "status": "unknown",
                "error": f"Checker não encontrado: {module_name}"
            }

        return checker.check()

    def calculate_overall_status(self, results: Dict[str, Any]) -> str:
        """
        Calcula status geral

        Args:
            results: Resultados dos checks

        Returns:
            str: Status geral (healthy/degraded/unhealthy)
        """
        statuses = [r.get("status", "unknown") for r in results.values()]

        # Se algum é unhealthy → overall unhealthy
        if "unhealthy" in statuses:
            return "unhealthy"

        # Se algum é degraded → overall degraded
        if "degraded" in statuses:
            return "degraded"

        # Se algum é error → overall degraded
        if "error" in statuses:
            return "degraded"

        # Senão, healthy
        return "healthy"

    def get_status(self, module_name: str = None) -> Dict[str, Any]:
        """
        Busca status (geral ou específico)

        Args:
            module_name: Nome do módulo (opcional)

        Returns:
            dict: Status
        """
        if module_name:
            return self.check_module(module_name)
        else:
            return self.check_all()

    def get_summary(self) -> Dict[str, Any]:
        """
        Busca resumo de health checks

        Returns:
            dict: Resumo
        """
        results = self.check_all()

        # Conta por status
        by_status = {}
        for result in results["modules"].values():
            status = result.get("status", "unknown")
            by_status[status] = by_status.get(status, 0) + 1

        return {
            "overall_status": results["overall_status"],
            "total_modules": len(results["modules"]),
            "by_status": by_status,
            "timestamp": datetime.now().isoformat()
        }

    def get_history(self, module_name: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca histórico de health checks

        Args:
            module_name: Nome do módulo (opcional)
            limit: Número máximo de resultados

        Returns:
            list: Histórico
        """
        # TODO: Implementar histórico
        return []

    def get_readiness(self) -> Dict[str, Any]:
        """
        Check de readiness (K8s)

        Returns:
            dict: Readiness
        """
        results = self.check_all()

        # Ready se todos são healthy
        is_ready = results["overall_status"] == "healthy"

        return {
            "ready": is_ready,
            "overall_status": results["overall_status"],
            "timestamp": datetime.now().isoformat()
        }

    def get_liveness(self) -> Dict[str, Any]:
        """
        Check de liveness (K8s)

        Returns:
            dict: Liveness
        """
        return {
            "alive": True,
            "timestamp": datetime.now().isoformat()
        }


# Exemplo de uso
if __name__ == "__main__":
    engine = HealthCheckEngine()

    # Check geral
    status = engine.get_status()
    print(f"\n🎯 Status geral: {status['overall_status']}")

    # Check específico
    redis_status = engine.check_module("redis")
    print(f"\n🔴 Redis status: {redis_status.get('status')}")

    # Resumo
    summary = engine.get_summary()
    print(f"\n📊 Resumo: {summary}")
