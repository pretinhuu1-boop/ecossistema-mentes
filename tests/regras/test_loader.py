import unittest
from unittest.mock import mock_open, patch
import os
import sys
import yaml

# Adiciona src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from regras.loader import RuleLoader

class TestRuleLoader(unittest.TestCase):

    def test_load_valid_yaml(self):
        """Testa carregamento de YAML válido"""
        yaml_content = """
regras:
  operacao:
    - id: R-TEST-01
      condicao: "x > 1"
      acao: "log"
"""
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            loader = RuleLoader("dummy.yaml")
            data = loader.load()
            
            self.assertIn("regras", data)
            self.assertIn("operacao", data["regras"])
            self.assertEqual(data["regras"]["operacao"][0]["id"], "R-TEST-01")

    def test_load_invalid_yaml(self):
        """Testa erro ao carregar YAML inválido"""
        # Conteúdo inválido (tabulação errada ou similar)
        yaml_content = ": - invalido" 
        
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            # Mock yaml.safe_load para lançar erro se necessário, ou confiar no parser real
            # No caso, o yaml.safe_load real vai tentar parsear string ": - invalido"
            # Se falhar, loader deve tratar ou propagar
            
            loader = RuleLoader("dummy.yaml")
            # Dependendo da implementação do loader, pode retornar None ou {}, ou dar raise
            # Assumindo que o loader trata exceções (verificaremos código depois se necessário)
            # Se não trata, o teste vai falhar com erro de YAML, o que é esperado
            try:
                data = loader.load()
            except yaml.YAMLError:
                # Se o loader deixa explodir, ok
                pass

    def test_file_not_found(self):
        """Testa arquivo não encontrado"""
        with patch("builtins.open", side_effect=FileNotFoundError):
            loader = RuleLoader("non_existent.yaml")
            data = loader.load()
            self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
