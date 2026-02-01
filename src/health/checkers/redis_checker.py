import redis
import os
from datetime import datetime
from typing import Dict, Any
from .base import BaseHealthChecker

class RedisHealthChecker(BaseHealthChecker):
    """Checker de saúde para o Redis"""

    def __init__(self):
        super().__init__("redis")
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.password = os.getenv("REDIS_PASSWORD", None)

    def check(self) -> Dict[str, Any]:
        """Executa check no Redis via ping()"""
        try:
            r = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                socket_timeout=2
            )
            if r.ping():
                info = r.info()
                details = {
                    "version": info.get("redis_version"),
                    "used_memory_human": info.get("used_memory_human"),
                    "connected_clients": info.get("connected_clients")
                }
                return self.create_success(details)
            else:
                return self.create_error("Redis ping returned False")
        except Exception as e:
            return self.create_error(str(e))
