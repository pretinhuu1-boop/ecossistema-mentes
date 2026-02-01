import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import time

# Adiciona src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from errors import robust_retry, ErrorClassifier, ErrorType

class TestErrorHandling(unittest.TestCase):

    def test_classifier(self):
        classifier = ErrorClassifier()
        
        # Test Timeout
        self.assertEqual(classifier.classify(TimeoutError("Timeout")), ErrorType.TRANSIENT)
        
        # Test KeyError
        self.assertEqual(classifier.classify(KeyError("Key")), ErrorType.PERMANENT)
        
        # Test Custom HTTP (Mock)
        mock_error = Exception("Rate limit")
        mock_error.response = MagicMock()
        mock_error.response.status_code = 429
        self.assertEqual(classifier.classify(mock_error), ErrorType.RATE_LIMIT)

    def test_robust_retry_success_after_failure(self):
        # Usamos uma lista para contar as chamadas
        calls = []

        @robust_retry(max_retries=2)
        def unstable_func():
            calls.append(1)
            if len(calls) < 2:
                raise ConnectionError("Falha temporária")
            return "Sucesso"

        # Patch do sleep para não demorar no teste
        with patch('time.sleep', return_value=None):
            result = unstable_func()
            self.assertEqual(result, "Sucesso")
            self.assertEqual(len(calls), 2)

    def test_robust_retry_max_retries_exceeded(self):
        calls = []

        @robust_retry(max_retries=2)
        def failing_func():
            calls.append(1)
            raise ConnectionError("Falha persistente")

        with patch('time.sleep', return_value=None):
            with self.assertRaises(ConnectionError):
                failing_func()
            
            # 1 tentativa original + 2 retries = 3 chamadas
            self.assertEqual(len(calls), 3)

if __name__ == '__main__':
    unittest.main()
