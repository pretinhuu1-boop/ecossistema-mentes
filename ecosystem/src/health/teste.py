#!/usr/bin/env python3
"""
Teste do Health Check Engine

Versão: 1.0
Data: 2026-01-31
"""

import os
import sys

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))

from engine import HealthCheckEngine


class SimulatedRedisChecker:
    """Checker simulado do Redis"""
    def check(self):
        """Check simulado"""
        return {
            "status": "healthy",
            "module": "redis",
            "timestamp": "2026-01-31T10:00:00",
            "details": {
                "ping": 1.0,
                "latency_ms": 0.5
            }
        }


class SimulatedCeleryChecker:
    """Checker simulado do Celery"""
    def check(self):
        """Check simulado"""
        return {
            "status": "healthy",
            "module": "celery",
            "timestamp": "2026-01-31T10:00:00",
            "details": {
                "workers": 4,
                "queues": 3
            }
        }


class SimulatedChromaChecker:
    """Checker simulado do ChromaDB"""
    def check(self):
        """Check simulado"""
        return {
            "status": "healthy",
            "module": "chroma",
            "timestamp": "2026-01-31T10:00:00",
            "details": {
                "collections": 5,
                "embeddings": 1000
            }
        }


class SimulatedRastreadorChecker:
    """Checker simulado do Rastreador"""
    def check(self):
        """Check simulado"""
        return {
            "status": "healthy",
            "module": "rastreador",
            "timestamp": "2026-01-31T10:00:00",
            "details": {
                "active_tasks": 2,
                "collected_sources": 5000
            }
        }


class SimulatedMineradorChecker:
    """Checker simulado do Minerador"""
    def check(self):
        """Check simulado"""
        return {
            "status": "healthy",
            "module": "minerador",
            "timestamp": "2026-01-31T10:00:00",
            "details": {
                "active_tasks": 3,
                "extracted_artifacts": 200
            }
        }


class SimulatedOrquestradorChecker:
    """Checker simulado do Orquestrador"""
    def check(self):
        """Check simulado"""
        return {
            "status": "healthy",
            "module": "orquestrador",
            "timestamp": "2026-01-31T10:00:00",
            "details": {
                "active_tasks": 1,
                "queued_tasks": 10
            }
        }


def test_health_engine():
    """Testa Health Check Engine"""
    print("🧪 Testando Health Check Engine...\n")

    # Inicia engine
    print("1️⃣ Inicializando engine...")
    engine = HealthCheckEngine()

    # Substitui checkers reais por simulados
    print("2️⃣ Substituindo checkers por simulados...")
    engine.checkers["redis"] = SimulatedRedisChecker()
    engine.checkers["celery"] = SimulatedCeleryChecker()
    engine.checkers["chroma"] = SimulatedChromaChecker()
    engine.checkers["rastreador"] = SimulatedRastreadorChecker()
    engine.checkers["minerador"] = SimulatedMineradorChecker()
    engine.checkers["orquestrador"] = SimulatedOrquestradorChecker()

    print(f"✅ Substituídos {len(engine.checkers)} checkers")

    # Check geral
    print("\n3️⃣ Executando check de todos os módulos...")
    status = engine.get_status()

    print(f"   Overall: {status['overall_status']}")
    print(f"   Timestamp: {status['timestamp']}")

    print("\n   Modules:")
    for module, module_status in status["modules"].items():
        print(f"      - {module}: {module_status.get('status', 'unknown')}")

    # Check específico
    print("\n4️⃣ Executando check do Redis...")
    redis_status = engine.check_module("redis")
    print(f"   Status: {redis_status.get('status', 'unknown')}")
    print(f"   Details: {redis_status.get('details', {})}")

    # Resumo
    print("\n5️⃣ Buscando resumo...")
    summary = engine.get_summary()

    print(f"   Total: {summary['total_modules']}")
    print(f"   Overall: {summary['overall_status']}")
    print(f"   Recent: {summary['recent_count']}")

    print("\n✅ Todos os testes passaram!")


if __name__ == "__main__":
    test_health_engine()
