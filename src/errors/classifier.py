import enum
from typing import Any

class ErrorType(enum.Enum):
    TRANSIENT = "transient"
    PERMANENT = "permanent"
    RATE_LIMIT = "rate_limit"
    UNKNOWN = "unknown"

class ErrorClassifier:
    """Classifica erros do sistema para decidir a estratégia de tratamento."""
    
    def classify(self, error: Exception) -> ErrorType:
        """Determina o tipo do erro baseado na exceção."""
        
        # Erros de Timeout -> Transient
        error_name = type(error).__name__.lower()
        if "timeout" in error_name or "connectionerror" in error_name:
            return ErrorType.TRANSIENT
            
        # Rate Limiting (Padrão OpenAI/Google/Comum) -> Rate Limit
        if "ratelimit" in error_name or "toomanyrequests" in error_name:
            return ErrorType.RATE_LIMIT
            
        # Erros de validação ou lógica -> Permanent
        if "valueerror" in error_name or "keyerror" in error_name or "notfound" in error_name:
            return ErrorType.PERMANENT
            
        # Erros HTTP (se a exceção tiver status_code)
        if hasattr(error, 'response') and hasattr(error.response, 'status_code'):
            sc = error.response.status_code
            if sc == 429:
                return ErrorType.RATE_LIMIT
            if 400 <= sc < 500:
                return ErrorType.PERMANENT
            if 500 <= sc < 600:
                return ErrorType.TRANSIENT
                
        return ErrorType.UNKNOWN
