import unittest
import os
import sys

# Adiciona src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from regras.parser import ConditionParser

class TestConditionParser(unittest.TestCase):

    def setUp(self):
        self.parser = ConditionParser()

    def test_greater_than(self):
        """Testa > """
        context = {"val": 10}
        self.assertTrue(self.parser.parse_and_eval("val > 5", context))
        self.assertFalse(self.parser.parse_and_eval("val > 15", context))

    def test_less_than(self):
        """Testa < """
        context = {"val": 10}
        self.assertTrue(self.parser.parse_and_eval("val < 15", context))
        self.assertFalse(self.parser.parse_and_eval("val < 5", context))

    def test_equals(self):
        """Testa =="""
        context = {"status": "ok"}
        self.assertTrue(self.parser.parse_and_eval("status == ok", context))
        self.assertFalse(self.parser.parse_and_eval("status == error", context))

    def test_variable_missing(self):
        """Testa variável faltando no contexto"""
        context = {}
        # Dependendo da implementação, pode retornar False ou dar erro
        # Assumindo False seguro
        self.assertFalse(self.parser.parse_and_eval("val > 5", context))

    def test_complex_condition(self):
        """Testa condição composta (se suportada) ou apenas robustez"""
        # Se o parser for simples regex, talvez não suporte AND/OR complexo nativamente
        # mas vamos testar se ele aguenta strings normais
        context = {"val": 10}
        self.assertTrue(self.parser.parse_and_eval("val >= 10", context))

if __name__ == '__main__':
    unittest.main()
