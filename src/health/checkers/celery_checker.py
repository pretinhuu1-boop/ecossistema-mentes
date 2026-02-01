import os
from celery import Celery
from datetime import datetime
from typing import Dict, Any
from .base import BaseHealthChecker

class CeleryHealthChecker(BaseHealthChecker):
    """Checker de saúde para o Celery"""

    def __init__(self):
        super().__init__("celery")
        self.broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

    def check(self) -> Dict[str, Any]:
        """Executa check no Celery verificando workers ativos"""
        try:
            app = Celery('health_check', broker=self.broker_url)
            inspect = app.control.inspect(timeout=2)
            active = inspect.active()
            
            if active is None:
                return self.create_error("No active Celery workers found or timeout")
            
            details = {
                "active_workers_count": len(active),
                "workers": list(active.keys())
            }
            return self.create_success(details)
        except Exception as e:
            return self.create_error(str(e))
