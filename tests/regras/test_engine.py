import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Adiciona src ao path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from regras.engine import RegrasEngine

class TestRegrasEngine(unittest.TestCase):

    def setUp(self):
        """Setup para cada teste"""
        self.mock_loader_patcher = patch('regras.engine.RuleLoader')
        self.mock_loader = self.mock_loader_patcher.start()
        
        self.mock_parser_patcher = patch('regras.engine.ConditionParser')
        self.mock_parser = self.mock_parser_patcher.start()
        
        self.mock_executor_patcher = patch('regras.engine.ActionExecutor')
        self.mock_executor = self.mock_executor_patcher.start()
        
        self.mock_logger_patcher = patch('regras.engine.RuleLogger')
        self.mock_logger = self.mock_logger_patcher.start()

        # Mock os.path.exists para sempre retornar True quando verificando arquivos de regras
        self.exists_patcher = patch('os.path.exists')
        self.mock_exists = self.exists_patcher.start()
        self.mock_exists.return_value = True

        # Configura retorno do loader mockado
        self.mock_loader_instance = self.mock_loader.return_value
        self.mock_loader_instance.load.return_value = {
            "regras": {
                "operacao": [
                    {
                        "id": "R-TEST-01",
                        "modulo": "teste",
                        "categoria": "operacao",
                        "condicao": "val > 10",
                        "acao": "log",
                        "prioridade": "alta"
                    }
                ]
            }
        }

    def tearDown(self):
        """Limpeza após cada teste"""
        self.mock_loader_patcher.stop()
        self.mock_parser_patcher.stop()
        self.mock_executor_patcher.stop()
        self.mock_logger_patcher.stop()
        self.exists_patcher.stop()

    def test_init_carrega_regras(self):
        """Testa se inicialização carrega regras corretamente"""
        engine = RegrasEngine(rules_dir="dummy_rules")
        
        # Verifica se tentou carregar os arquivos esperados
        self.assertTrue(self.mock_loader.called)
        self.assertIn("ecossistema", engine.rules)
        self.assertIn("rag", engine.rules)

    def test_count_rules(self):
        """Testa contagem de regras"""
        engine = RegrasEngine()
        # Temos 2 arquivos simulados (ecossistema, rag), cada um retornando 1 regra no mock
        # Total = 1 + 1 = 2
        self.assertEqual(engine.count_rules(), 2)

    def test_evaluate_executa_acao_quando_condicao_verdadeira(self):
        """Testa avaliação quando condição é verdadeira"""
        engine = RegrasEngine()
        
        # Mock parser retorna True
        engine.parser.parse_and_eval.return_value = True
        
        # Contexto dummy
        contexto = {"modulo": "teste", "val": 15}
        
        # Executa
        acoes = engine.evaluate(contexto)
        
        # Verifica se executou ação
        self.assertEqual(len(acoes), 2) # 1 do ecossistema + 1 do rag (pq mock retorna mesmo dict)
        self.assertTrue(engine.executor.execute.called)
        self.assertTrue(engine.logger.log.called)

    def test_evaluate_nao_executa_quando_condicao_falsa(self):
        """Testa avaliação quando condição é falsa"""
        engine = RegrasEngine()
        
        # Mock parser retorna False
        engine.parser.parse_and_eval.return_value = False
        
        # Contexto dummy
        contexto = {"modulo": "teste", "val": 5}
        
        # Executa
        acoes = engine.evaluate(contexto)
        
        # Verifica que NÃO executou ação
        self.assertEqual(len(acoes), 0)
        self.assertFalse(engine.executor.execute.called)

    def test_evaluate_filtra_por_modulo(self):
        """Testa se filtra regras irrelevantes para o módulo"""
        engine = RegrasEngine()
        
        # Contexto de outro módulo
        contexto = {"modulo": "outro_modulo"}
        
        # Regra mockada tem modulo="teste", então deve ser filtrada antes de avaliar
        engine.evaluate(contexto)
        
        # Parser não deve nem ser chamado se foi filtrado
        self.assertFalse(engine.parser.parse_and_eval.called)

    def test_reload(self):
        """Testa reload de regras"""
        engine = RegrasEngine()
        self.mock_loader.reset_mock()
        
        engine.reload()
        
        # Deve chamar loader novamente
        self.assertTrue(self.mock_loader.called)

if __name__ == '__main__':
    unittest.main()
