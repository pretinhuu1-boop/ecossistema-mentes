"""
Health Check Engine

Versão: 1.0
Data: 2026-01-31
"""

from .engine import HealthCheckEngine
from .checkers.base import BaseHealthChecker, HealthChecker
from .api import HealthAPI
from .scheduler import HealthCheckScheduler
from .alerts import AlertManager
from .prometheus import HealthCheckPrometheus


# Exemplo de uso
if __name__ == "__main__":
    # Inicia engine
    engine = HealthCheckEngine()

    # Check geral
    status = engine.get_status()

    print(f"\n🏥 Health Status:")
    print(f"   Overall: {status['overall_status']}")
    print(f"   Timestamp: {status['timestamp']}")

    print(f"\n📊 Modules:")
    for module, module_status in status["modules"].items():
        print(f"   - {module}: {module_status.get('status', 'unknown')}")
