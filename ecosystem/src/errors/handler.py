import functools
import logging
from typing import Dict, Any, Callable
from .classifier import ErrorClassifier, ErrorType
from .backoff import ExponentialBackoff
from .log import ErrorLog

class RobustErrorHandler:
    """Coordenador central de tratamento de erros."""
    
    def __init__(self):
        self.classifier = ErrorClassifier()
        self.backoff = ExponentialBackoff()
        self.log_manager = ErrorLog()
        
    def handle(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Trata o erro e decide a ação (retry ou abort)."""
        error_type = self.classifier.classify(error)
        self.log_manager.log(error, error_type.value, context)
        
        retry_count = context.get("retry_count", 0)
        max_retries = context.get("max_retries", 3)
        
        if error_type in [ErrorType.TRANSIENT, ErrorType.RATE_LIMIT]:
            if retry_count < max_retries:
                wait_time = self.backoff.calculate(retry_count)
                print(f"⚠️ Erro {error_type.value} detectado: {error}. Tentativa {retry_count+1}/{max_retries}. Esperando {wait_time:.2f}s...")
                return {
                    "action": "retry",
                    "wait_time": wait_time,
                    "new_context": {**context, "retry_count": retry_count + 1}
                }
        
        # Falha definitiva ou erro permanente
        print(f"❌ Erro fatal ou limite de retries atingido: {error}")
        return {"action": "abort", "reason": str(error)}

def robust_retry(max_retries: int = 3):
    """Decorator para integrar o RobustErrorHandler facilmente."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            handler = RobustErrorHandler()
            context = {
                "module": func.__module__,
                "function": func.__name__,
                "max_retries": max_retries,
                "retry_count": 0
            }
            
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    result = handler.handle(e, context)
                    if result["action"] == "retry":
                        context = result["new_context"]
                        self_backoff = ExponentialBackoff()
                        self_backoff.wait(context["retry_count"] - 1)
                        continue
                    else:
                        raise e
        return wrapper
    return decorator
