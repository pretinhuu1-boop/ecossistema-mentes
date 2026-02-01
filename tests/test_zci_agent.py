import unittest
import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from zci_agent.core import ZCIAgent
from zci_agent.server import app

class TestZCIAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ZCIAgent()
        self.app = app.test_client()
        self.app.testing = True

    def test_generate_description_success(self):
        desc = self.agent.generate_description("Perfume X", ["floral", "fresh"])
        self.assertIn("Perfume X", desc)
        # Check if at least one attribute or template part is present
        # Since implementation uses random choice, we check basic structure
        self.assertIsInstance(desc, str)
        self.assertGreater(len(desc), 10)

    def test_generate_description_empty(self):
        desc = self.agent.generate_description("", [])
        self.assertEqual(desc, "Please provide a product name.")

    def test_optimize_seo_success(self):
        text = "This is a great product."
        keywords = ["best", "quality"]
        optimized = self.agent.optimize_seo(text, keywords)
        self.assertIn("best", optimized)
        self.assertIn("quality", optimized)

    def test_optimize_seo_already_optimized(self):
        text = "This is the best quality product."
        keywords = ["best", "quality"]
        optimized = self.agent.optimize_seo(text, keywords)
        self.assertEqual(optimized, text)

    def test_api_health(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'healthy')

    def test_api_generate(self):
        response = self.app.post('/api/zci/generate', 
                                 data=json.dumps({"product_name": "Test Product", "attributes": ["attr1"]}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Product", response.get_json()['description'])

if __name__ == '__main__':
    unittest.main()
