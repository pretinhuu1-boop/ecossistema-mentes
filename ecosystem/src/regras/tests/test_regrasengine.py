#!/usr/bin/env python3
"""
Unit Tests para RegrasEngine

Versão: 1.0
Data: 2026-01-31
"""

import sys
import os
import unittest
import tempfile
import shutil

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from regras.engine import RegrasEngine
from regras.loader import RuleLoader, RuleSchemaError
from regras.parser import ConditionParser, ConditionParseError, ConditionEvalError
from regras.actions import ActionExecutor


class TestRuleLoader(unittest.TestCase):
    """Unit tests para RuleLoader"""

    def setUp(self):
        """Setup antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Cleanup depois de cada teste"""
        shutil.rmtree(self.temp_dir)

    def test_load_valid_yaml(self):
        """Testa carregar YAML válido"""
        yaml_content = """
regras:
  operacao:
    - id: TEST-01
      modulo: rastreador
      categoria: operacao
      condicao: "x >= 10"
      acao: parar
      prioridade: alta
      descricao: Test rule
"""
        yaml_path = os.path.join(self.temp_dir, "test.yaml")
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)

        loader = RuleLoader(yaml_path)
        data = loader.load()

        self.assertIn("regras", data)
        self.assertEqual(len(data["regras"]["operacao"]), 1)

    def test_load_missing_regras_key(self):
        """Testa erro quando falta chave 'regras'"""
        yaml_content = """
invalid:
  - id: TEST-01
"""
        yaml_path = os.path.join(self.temp_dir, "test.yaml")
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)

        loader = RuleLoader(yaml_path)

        with self.assertRaises(RuleSchemaError):
            loader.load()

    def test_load_invalid_regras_type(self):
        """Testa erro quando 'regras' não é dict"""
        yaml_content = """
regras:
  - id: TEST-01
"""
        yaml_path = os.path.join(self.temp_dir, "test.yaml")
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)

        loader = RuleLoader(yaml_path)

        with self.assertRaises(RuleSchemaError):
            loader.load()

    def test_load_missing_required_fields(self):
        """Testa erro quando faltam campos obrigatórios"""
        yaml_content = """
regras:
  operacao:
    - id: TEST-01
      modulo: rastreador
      categoria: operacao
      # Falta condicao e acao
"""
        yaml_path = os.path.join(self.temp_dir, "test.yaml")
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)

        loader = RuleLoader(yaml_path)

        with self.assertRaises(RuleSchemaError):
            loader.load()

    def test_load_multiple_categories(self):
        """Testa carregar múltiplas categorias"""
        yaml_content = """
regras:
  operacao:
    - id: TEST-OP-01
      modulo: rastreador
      categoria: operacao
      condicao: "x >= 10"
      acao: parar
  qualidade:
    - id: TEST-QF-01
      modulo: rastreador
      categoria: qualidade
      condicao: "y < 0.5"
      acao: rejeitar
"""
        yaml_path = os.path.join(self.temp_dir, "test.yaml")
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)

        loader = RuleLoader(yaml_path)
        data = loader.load()

        self.assertEqual(len(data["regras"]["operacao"]), 1)
        self.assertEqual(len(data["regras"]["qualidade"]), 1)


class TestConditionParser(unittest.TestCase):
    """Unit tests para ConditionParser"""

    def setUp(self):
        """Setup antes de cada teste"""
        self.parser = ConditionParser()

    def test_parse_greater_than_or_equal(self):
        """Testa parser de >="""
        condition = "sources_collected >= 10000"
        left, op, right = self.parser.parse(condition)

        self.assertEqual(left, "sources_collected")
        self.assertEqual(op, ">=")
        self.assertEqual(right, "10000")

    def test_parse_less_than(self):
        """Testa parser de <"""
        condition = "quality_score < 0.7"
        left, op, right = self.parser.parse(condition)

        self.assertEqual(left, "quality_score")
        self.assertEqual(op, "<")
        self.assertEqual(right, "0.7")

    def test_parse_in(self):
        """Testa parser de in"""
        condition = "tag in ['video', 'youtube']"
        left, op, right = self.parser.parse(condition)

        self.assertEqual(left, "tag")
        self.assertEqual(op, "in")
        self.assertEqual(right, "['video', 'youtube']")

    def test_eval_greater_than_or_equal(self):
        """Testa avaliação de >="""
        contexto = {"sources_collected": 10000, "max_sources": 10000}
        condition = "sources_collected >= max_sources"
        result = self.parser.parse_and_eval(condition, contexto)

        self.assertTrue(result)

    def test_eval_less_than(self):
        """Testa avaliação de <"""
        contexto = {"quality_score": 0.5, "min_quality": 0.7}
        condition = "quality_score < min_quality"
        result = self.parser.parse_and_eval(condition, contexto)

        self.assertTrue(result)

    def test_eval_equals(self):
        """Testa avaliação de =="""
        contexto = {"status": "stopped", "expected_status": "stopped"}
        condition = "status == expected_status"
        result = self.parser.parse_and_eval(condition, contexto)

        self.assertTrue(result)

    def test_eval_in(self):
        """Testa avaliação de in"""
        contexto = {"tag": "video", "tags": ["video", "youtube"]}
        condition = "tag in tags"
        result = self.parser.parse_and_eval(condition, contexto)

        self.assertTrue(result)

    def test_eval_not_in(self):
        """Testa avaliação de not in"""
        contexto = {"tag": "image", "tags": ["video", "youtube"]}
        condition = "tag not in tags"
        result = self.parser.parse_and_eval(condition, contexto)

        self.assertTrue(result)

    def test_eval_dotted_notation(self):
        """Testa avaliação com notação de ponto"""
        contexto = {
            "metrics": {
                "confidence_mean": 0.6
            },
            "min_confidence": 0.7
        }
        condition = "metrics.confidence_mean < min_confidence"
        result = self.parser.parse_and_eval(condition, contexto)

        self.assertTrue(result)

    def test_parse_invalid_condition(self):
        """Testa erro ao parsear condição inválida"""
        condition = "invalid condition"

        with self.assertRaises(ConditionParseError):
            self.parser.parse(condition)

    def test_eval_missing_variable(self):
        """Testa avaliação com variável faltando"""
        contexto = {"x": 10}
        condition = "x >= y"  # y não existe

        result = self.parser.parse_and_eval(condition, contexto)
        self.assertFalse(result)  # None >= 10 é False

    def test_has_comparator(self):
        """Testa detecção de comparador"""
        self.assertTrue(self.parser.has_comparator("x >= y"))
        self.assertTrue(self.parser.has_comparator("tag in [a, b]"))
        self.assertFalse(self.parser.has_comparator("is_spam"))

    def test_resolve_variable_number(self):
        """Testa resolução de variável numérica"""
        var = "100"
        result = self.parser.resolve_variable(var, {})

        self.assertEqual(result, 100.0)

    def test_resolve_variable_from_context(self):
        """Testa resolução de variável do contexto"""
        contexto = {"x": 10}
        result = self.parser.resolve_variable("x", contexto)

        self.assertEqual(result, 10)

    def test_resolve_variable_dotted(self):
        """Testa resolução de variável com notação de ponto"""
        contexto = {"metrics": {"x": 10}}
        result = self.parser.resolve_variable("metrics.x", contexto)

        self.assertEqual(result, 10)


class TestActionExecutor(unittest.TestCase):
    """Unit tests para ActionExecutor"""

    def setUp(self):
        """Setup antes de cada teste"""
        self.executor = ActionExecutor()

    def test_action_parar(self):
        """Testa ação parar"""
        rule = {
            "id": "TEST-01",
            "acao": "parar",
            "descricao": "Test stop"
        }
        contexto = {
            "modulo": "rastreador",
            "data_id": "source_001"
        }

        result = self.executor.execute("parar", rule, contexto)

        self.assertEqual(result["status"], "stopped")
        self.assertEqual(result["modulo"], "rastreador")

    def test_action_rejeitar(self):
        """Testa ação rejeitar"""
        rule = {
            "id": "TEST-02",
            "acao": "rejeitar",
            "descricao": "Test reject"
        }
        contexto = {
            "data_id": "artifact_001"
        }

        result = self.executor.execute("rejeitar", rule, contexto)

        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["data_id"], "artifact_001")

    def test_action_retry_com_backoff_first_attempt(self):
        """Testa ação retry_com_backoff (primeira tentativa)"""
        rule = {
            "id": "TEST-03",
            "acao": "retry_com_backoff",
            "max_retries": 3
        }
        contexto = {
            "retry_count": 0
        }

        result = self.executor.execute("retry_com_backoff", rule, contexto)

        self.assertEqual(result["status"], "retrying")
        self.assertEqual(result["new_retry_count"], 1)
        self.assertGreater(result["wait_time"], 0)

    def test_action_retry_com_backoff_max_retries(self):
        """Testa ação retry_com_backoff (máximo atingido)"""
        rule = {
            "id": "TEST-04",
            "acao": "retry_com_backoff",
            "max_retries": 3
        }
        contexto = {
            "retry_count": 3
        }

        result = self.executor.execute("retry_com_backoff", rule, contexto)

        self.assertEqual(result["status"], "max_retries_exceeded")
        self.assertEqual(result["retry_count"], 3)

    def test_action_alert(self):
        """Testa ação alert"""
        rule = {
            "id": "TEST-05",
            "acao": "alert",
            "descricao": "Test alert"
        }
        contexto = {}

        result = self.executor.execute("alert", rule, contexto)

        self.assertEqual(result["status"], "alert_sent")
        self.assertEqual(result["rule_id"], "TEST-05")

    def test_unknown_action(self):
        """Testa ação desconhecida"""
        rule = {"id": "TEST-06"}
        contexto = {}

        result = self.executor.execute("unknown_action", rule, contexto)

        self.assertEqual(result["status"], "unknown_action")

    def test_calculate_backoff(self):
        """Testa cálculo de backoff"""
        # 2^0 = 1 (com jitter, vai ser ~1.0)
        wait_time = self.executor.calculate_backoff(0)
        self.assertGreaterEqual(wait_time, 1.0)
        self.assertLess(wait_time, 1.2)  # jitter de até 10%

        # 2^1 = 2 (com jitter, vai ser ~2.0)
        wait_time = self.executor.calculate_backoff(1)
        self.assertGreaterEqual(wait_time, 2.0)
        self.assertLess(wait_time, 2.3)

        # 2^2 = 4 (com jitter, vai ser ~4.0)
        wait_time = self.executor.calculate_backoff(2)
        self.assertGreaterEqual(wait_time, 4.0)
        self.assertLess(wait_time, 4.5)

        # 2^10 = 1024, mas max é 60
        wait_time = self.executor.calculate_backoff(10)
        self.assertEqual(wait_time, 60.0)

        # Teste sem jitter (múltiplos pequenos)
        wait_time = self.executor.calculate_backoff(3)
        self.assertGreaterEqual(wait_time, 8.0)
        self.assertLess(wait_time, 9.0)


class TestRegrasEngine(unittest.TestCase):
    """Unit tests para RegrasEngine"""

    def setUp(self):
        """Setup antes de cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.rules_dir = os.path.join(self.temp_dir, "rules")
        os.makedirs(self.rules_dir)

        # Cria arquivo de regras de teste
        yaml_content = """
regras:
  operacao:
    - id: TEST-OP-01
      modulo: rastreador
      categoria: operacao
      condicao: "sources_collected >= max_sources"
      acao: parar
      prioridade: alta
      descricao: Para quando atinge max_sources

    - id: TEST-OP-02
      modulo: minerador
      categoria: operacao
      condicao: "confidence_mean < 0.7"
      acao: parar
      prioridade: alta
      descricao: Para quando min_confidence_mean < 0.7

  qualidade:
    - id: TEST-QF-01
      modulo: rastreador
      categoria: qualidade
      condicao: "quality_score < 0.7"
      acao: rejeitar
      prioridade: alta
      descricao: Rejeita fontes com quality < 0.7
"""
        yaml_path = os.path.join(self.rules_dir, "ecossistema.yaml")
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)

        self.engine = RegrasEngine(rules_dir=self.rules_dir)

    def tearDown(self):
        """Cleanup depois de cada teste"""
        shutil.rmtree(self.temp_dir)

    def test_load_rules(self):
        """Testa carregamento de regras"""
        # Chama count_rules diretamente do engine
        total_manual = 0
        for rule_set in self.engine.rules.values():
            regras_dict = rule_set.get('regras', {})
            if isinstance(regras_dict, dict):
                for regras in regras_dict.values():
                    if isinstance(regras, list):
                        total_manual += len(regras)
        
        total = self.engine.count_rules()
        print(f"  Total manual: {total_manual}")
        print(f"  Total count_rules(): {total}")
        
        # Debug: print engine.rules
        print(f"  engine.rules: {self.engine.rules}")
        
        self.assertEqual(total, 3)
        self.assertEqual(total_manual, 3)

    def test_get_rules_by_category(self):
        """Testa busca por categoria"""
        operacao_rules = self.engine.get_rules_by_category("operacao")
        self.assertEqual(len(operacao_rules), 2)

        qualidade_rules = self.engine.get_rules_by_category("qualidade")
        self.assertEqual(len(qualidade_rules), 1)

    def test_get_rules_by_module(self):
        """Testa busca por módulo"""
        rastreador_rules = self.engine.get_rules_by_module("rastreador")
        self.assertEqual(len(rastreador_rules), 2)

        minerador_rules = self.engine.get_rules_by_module("minerador")
        self.assertEqual(len(minerador_rules), 1)

    def test_evaluate_context_with_match(self):
        """Testa avaliação de contexto (com match)"""
        contexto = {
            "modulo": "rastreador",
            "sources_collected": 10000,
            "max_sources": 10000,
            "data_id": "source_001"
        }

        acoes = self.engine.evaluate(contexto)

        self.assertGreater(len(acoes), 0)
        stop_actions = [a for a in acoes if a["acao"] == "parar"]
        self.assertGreater(len(stop_actions), 0)

    def test_evaluate_context_no_match(self):
        """Testa avaliação de contexto (sem match)"""
        contexto = {
            "modulo": "rastreador",
            "sources_collected": 100,
            "max_sources": 10000,
            "quality_score": 0.9,
            "data_id": "source_001"
        }

        acoes = self.engine.evaluate(contexto)

        # Nenhuma ação deve ser executada
        self.assertEqual(len(acoes), 0)

    def test_prioridade_alta(self):
        """Testa priorização (alta)"""
        contexto = {
            "modulo": "rastreador",
            "sources_collected": 10000,
            "max_sources": 10000,
            "quality_score": 0.5,
            "data_id": "source_001"
        }

        acoes = self.engine.evaluate(contexto)

        # Primeira ação deve ser "parar" (prioridade alta)
        self.assertEqual(acoes[0]["acao"], "parar")

    def test_reload(self):
        """Testa reload de regras"""
        count_before = self.engine.count_rules()

        # Modifica arquivo de regras
        yaml_content = """
regras:
  operacao:
    - id: TEST-OP-NEW
      modulo: rastreador
      categoria: operacao
      condicao: "x >= 10"
      acao: parar
"""
        yaml_path = os.path.join(self.rules_dir, "ecossistema.yaml")
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)

        # Recarrega
        self.engine.reload()
        count_after = self.engine.count_rules()

        # Deve ter mudado
        self.assertNotEqual(count_before, count_after)


if __name__ == '__main__':
    unittest.main(verbosity=2)
