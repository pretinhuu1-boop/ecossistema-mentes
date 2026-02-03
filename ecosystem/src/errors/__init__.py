"""
Módulo Errors (GAP 12) - Ecossistema de Mentes
"""
from .classifier import ErrorClassifier, ErrorType
from .backoff import ExponentialBackoff
from .log import ErrorLog
from .handler import RobustErrorHandler, robust_retry
