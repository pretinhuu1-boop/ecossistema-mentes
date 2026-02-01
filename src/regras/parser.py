"""
ConditionParser — Parser e avaliação de condições

Versão: 1.0
Data: 2026-01-31
"""

import re


class ConditionParseError(Exception):
    """Erro ao parsear condição"""
    pass


class ConditionEvalError(Exception):
    """Erro ao avaliar condição"""
    pass


class ConditionParser:
    """Parser e avaliação de condições"""

    # Comparadores suportados (ordenados por comprimento - longos primeiro)
    COMPARATORS = [
        " not in ", " >= ", " <= ", " == ", " != ", " in ", " > ", " < "
    ]

    def parse_and_eval(self, condition: str, contexto: dict) -> bool:
        """
        Parser e avaliação de condições

        Args:
            condition: String de condição ("sources_collected >= max_sources")
            contexto: dict com contexto

        Returns:
            bool: Resultado da avaliação
        """
        try:
            # Se condição é simples (sem comparadores)
            if not self.has_comparator(condition):
                # Verifica se é True em contexto
                return contexto.get(condition, False)

            # Parse condição
            left, op, right = self.parse(condition)

            # Resolve variáveis
            left_value = self.resolve_variable(left, contexto)
            right_value = self.resolve_variable(right, contexto)

            # Se qualquer valor é None, retorna False
            if left_value is None or right_value is None:
                return False

            # Avalia
            result = self.eval_comparison(left_value, op, right_value)

            return result

        except Exception as e:
            print(f"❌ Erro ao avaliar condição '{condition}': {e}")
            raise ConditionEvalError(f"Error evaluating condition: {e}")

    def has_comparator(self, condition: str) -> bool:
        """Verifica se condição tem comparador"""
        return any(comp in condition for comp in self.COMPARATORS) or \
               any(comp in condition for comp in [">=", "<=", ">", "<", "==", "!="])

    def parse(self, condition: str) -> tuple:
        """
        Parse condição em left, op, right

        Args:
            condition: String de condição

        Returns:
            tuple: (left, op, right)
        """
        # Tenta comparadores com espaço primeiro (not in, in, >=, <=, ==, !=)
        for comp in self.COMPARATORS:
            if comp in condition:
                parts = condition.split(comp)
                if len(parts) == 2:
                    return parts[0].strip(), comp.strip(), parts[1].strip()

        # Tenta comparadores sem espaço (>, <)
        for comp in [">", "<"]:
            if comp in condition and comp not in [" > ", " < "]:
                # Verifica se não é parte de >= ou <=
                if ">=" not in condition and "<=" not in condition:
                    parts = condition.split(comp)
                    if len(parts) == 2:
                        return parts[0].strip(), comp.strip(), parts[1].strip()

        raise ConditionParseError(f"Could not parse condition: {condition}")

    def resolve_variable(self, var: str, contexto: dict):
        """
        Resolve variável do contexto

        Args:
            var: Variável para resolver
            contexto: Contexto

        Returns:
            Valor da variável (int, float, str, etc.)
        """
        # Se é número, retorna como número
        try:
            return float(var)
        except ValueError:
            pass

        # Se é string, busca em contexto
        # Suporta notação de ponto (e.g., metrics.sources_collected)
        if "." in var:
            parts = var.split(".")
            value = contexto
            for part in parts:
                value = value.get(part, None)
                if value is None:
                    return None
            return value
        else:
            return contexto.get(var, None)

    def eval_comparison(self, left, op: str, right):
        """
        Avalia comparação

        Args:
            left: Valor esquerda
            op: Operador
            right: Valor direita

        Returns:
            bool: Resultado da comparação
        """
        if op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        elif op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "in":
            return left in right
        elif op == "not in":
            return left not in right
        else:
            raise ConditionEvalError(f"Unknown operator: {op}")


# Exemplo de uso
if __name__ == "__main__":
    parser = ConditionParser()

    # Exemplo 1: Comparação simples
    contexto1 = {
        "sources_collected": 10000,
        "max_sources": 10000
    }
    condicao1 = "sources_collected >= max_sources"
    result1 = parser.parse_and_eval(condicao1, contexto1)
    print(f"{condicao1} = {result1}")

    # Exemplo 2: Notação de ponto
    contexto2 = {
        "metrics": {
            "confidence_mean": 0.7
        },
        "min_confidence": 0.7
    }
    condicao2 = "metrics.confidence_mean < min_confidence"
    result2 = parser.parse_and_eval(condicao2, contexto2)
    print(f"{condicao2} = {result2}")

    # Exemplo 3: in/not in
    contexto3 = {
        "tags": ["video", "youtube"],
        "target_tag": "youtube"
    }
    condicao3 = "target_tag in tags"
    result3 = parser.parse_and_eval(condicao3, contexto3)
    print(f"{condicao3} = {result3}")
