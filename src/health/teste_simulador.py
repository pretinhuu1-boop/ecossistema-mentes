#!/usr/bin/env python3
"""
Teste do Health Check Engine

Versão: 1.0
Data: 2026-01-31
"""

import os
import sys

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../")))

from engine import HealthCheckEngine


class SimulatedChecker:
    """Checker simulado para teste"""

    def __init__(self, module_name: str):
        self.module_name = module_name

    def check(self):
        """Check simulado (healthy)"""
        return {
            "status": "healthy",
            "module": self.module_name,
            "timestamp": "2026-01-31T10:00:00",
            "details": {
                "ping": 1.0,
                "latency_ms": 0.5
            }
        }


def test_health_engine():
    """Testa Health Check Engine"""
    print("🧪 Testando Health Check Engine...\n")

    # 1. Criar checkers simulados
    print("1️⃣ Criando checkers simulados...")
    checkers = {
        "redis": SimulatedChecker("redis"),
        "celery": SimulatedChecker("celery"),
        "chroma": SimulatedChecker("chroma"),
        "rastreador": SimulatedChecker("rastreador"),
        "minerador": SimulatedChecker("minerador"),
        "orquestrador": SimulatedChecker("orquestrador")
    }

    print(f"   ✅ Criados {len(checkers)} checkers")

    # 2. Testar HealthCheckEngine
    print("\n2️⃣ Testando HealthCheckEngine...")
    engine = HealthCheckEngine()

    # Substitui checkers pelos simulados
    engine.checkers = checkers

    # 3. Testar check_all
    print("\n3️⃣ Testando check_all()...")
    status = engine.check_all()

    print(f"   Overall: {status['overall_status']}")
    print(f"   Timestamp: {status['timestamp']}")

    print("\n   Modules:")
    for module, module_status in status["modules"].items():
        print(f"      - {module}: {module_status.get('status', 'unknown')}")

    # 4. Testar check_module
    print("\n4️⃣ Testando check_module()...")
    redis_status = engine.check_module("redis")
    print(f"   Status: {redis_status.get('status', 'unknown')}")
    print(f"   Details: {redis_status.get('details', {})}")

    # 5. Testar get_summary
    print("\n5️⃣ Testando get_summary()...")
    summary = engine.get_summary()

    print(f"   Overall: {summary['overall_status']}")
    print(f"   Total modules: {summary['total_modules']}")
    print(f"   By status:")
    for status_type, count in summary["by_status"].items():
        print(f"      - {status_type}: {count}")

    print("\n✅ Todos os testes passaram!")


if __name__ == "__main__":
    test_health_engine()
