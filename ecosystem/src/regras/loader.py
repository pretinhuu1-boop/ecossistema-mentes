"""
RuleLoader — Carrega regras de arquivos YAML

Versão: 1.0
Data: 2026-01-31
"""

import yaml


class RuleSchemaError(Exception):
    """Erro no esquema de regras"""
    pass


class RuleLoader:
    """Carrega regras de arquivos YAML"""

    def __init__(self, path: str):
        """
        Inicializa RuleLoader

        Args:
            path: Caminho do arquivo YAML
        """
        self.path = path

    def load(self) -> dict:
        """
        Carrega regras do arquivo YAML

        Returns:
            dict: Regras carregadas
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Valida esquema
            self.validate_schema(data)

            return data

        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {self.path}")
            return None
        except yaml.YAMLError as e:
            print(f"❌ Erro ao parsear YAML: {e}")
            return None

    def validate_schema(self, data: dict):
        """
        Valida esquema de regras

        Args:
            data: Dados carregados do YAML

        Raises:
            RuleSchemaError: Se esquema inválido
        """
        # Se está completamente vazio, skip validação (arquivo não encontrado)
        if not data:
            return

        # Verifica se tem "regras"
        if "regras" not in data:
            raise RuleSchemaError("Arquivo deve conter 'regras'")

        # Verifica se é dict (categorias → lista de regras)
        if not isinstance(data["regras"], dict):
            raise RuleSchemaError("'regras' deve ser um dict de categorias")

        # Se regras é vazio {}, isso é válido (arquivo de regras vazio)
        if not data["regras"]:
            return

        # Verifica se cada regra tem campos obrigatórios
        required_fields = ["id", "modulo", "categoria", "condicao", "acao"]

        for category, rules in data["regras"].items():
            if not isinstance(rules, list):
                raise RuleSchemaError(f"Categoria '{category}' deve ser uma lista")

            for rule in rules:
                for field in required_fields:
                    if field not in rule:
                        raise RuleSchemaError(
                            f"Regra {rule.get('id', 'unknown')} "
                            f"missing field: {field}"
                        )


# Exemplo de uso
if __name__ == "__main__":
    # Carrega arquivo de exemplo
    loader = RuleLoader("rules/ecossistema.yaml")
    data = loader.load()

    print(f"✅ Regras carregadas: {len(data.get('regras', []))}")
    for rule in data.get("regras", [])[:5]:
        print(f"  - {rule['id']}: {rule['acao']}")
