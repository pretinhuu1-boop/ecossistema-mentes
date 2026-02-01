import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from health.checkers.redis_checker import RedisHealthChecker
from health.checkers.celery_checker import CeleryHealthChecker
from health.checkers.chroma_checker import ChromaHealthChecker

class TestHealthCheckers(unittest.TestCase):

    @patch('redis.Redis')
    def test_redis_checker_healthy(self, mock_redis):
        # Configura mock
        mock_instance = mock_redis.return_value
        mock_instance.ping.return_value = True
        mock_instance.info.return_value = {"redis_version": "7.0.0", "used_memory_human": "1MB", "connected_clients": 5}
        
        checker = RedisHealthChecker()
        result = checker.check()
        
        self.assertEqual(result['status'], 'healthy')
        self.assertEqual(result['details']['version'], '7.0.0')

    @patch('redis.Redis')
    def test_redis_checker_unhealthy(self, mock_redis):
        mock_instance = mock_redis.return_value
        mock_instance.ping.side_effect = Exception("Connection refused")
        
        checker = RedisHealthChecker()
        result = checker.check()
        
        self.assertEqual(result['status'], 'unhealthy')
        self.assertIn("Connection refused", result['error'])

    @patch('celery.Celery')
    def test_celery_checker_healthy(self, mock_celery):
        mock_app = mock_celery.return_value
        mock_inspect = mock_app.control.inspect.return_value
        mock_inspect.active.return_value = {"worker1@host": []}
        
        checker = CeleryHealthChecker()
        result = checker.check()
        
        self.assertEqual(result['status'], 'healthy')
        self.assertEqual(result['details']['active_workers_count'], 1)

    @patch('chromadb.PersistentClient')
    def test_chroma_checker_healthy(self, mock_chroma):
        mock_client = mock_chroma.return_value
        mock_client.heartbeat.return_value = 123456789
        mock_client.list_collections.return_value = []
        
        checker = ChromaHealthChecker()
        result = checker.check()
        
        self.assertEqual(result['status'], 'healthy')
        self.assertEqual(result['details']['heartbeat'], 123456789)

if __name__ == '__main__':
    unittest.main()
