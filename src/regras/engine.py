"""
RegrasEngine — Motor de Execução de Regras

Versão: 1.0
Data: 2026-01-31
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Any

from .loader import RuleLoader
from .parser import ConditionParser
from .actions import ActionExecutor
from .logger import RuleLogger


class RegrasEngine:
    """Motor de execução de 212 regras do ecossistema"""

    def __init__(self, rules_dir="rules"):
        """
        Inicializa RegrasEngine

        Args:
            rules_dir: Diretório dos arquivos de regras (padrão: "rules")
        """
        self.rules_dir = rules_dir
        self.rules = {}
        self.logger = RuleLogger()
        self.parser = ConditionParser()
        self.executor = ActionExecutor()

        # Carrega regras
        self.load_all_rules()

    def load_all_rules(self):
        """Carrega todas as regras do diretório"""
        print("📥 Carregando regras...")

        rule_files = {
            "ecossistema": f"{self.rules_dir}/ecossistema.yaml",
            "rag": f"{self.rules_dir}/rag.yaml"
        }

        for name, path in rule_files.items():
            if os.path.exists(path):
                rule_data = self.load_rules(path)
                if rule_data:  # Só adiciona se não for None
                    self.rules[name] = rule_data
                    total = sum(len(regras) for regras in self.rules[name].get('regras', {}).values())
                    print(f"✅ {name}: {total} regras")
            else:
                print(f"⚠️ {name}: arquivo não encontrado ({path})")

        total_rules = sum(
            sum(len(regras) for regras in rs.get('regras', {}).values())
            for rs in self.rules.values()
        )
        print(f"🎯 Total: {total_rules} regras carregadas")

    def count_rules(self) -> int:
        """Cont total de regras carregadas"""
        total = 0
        for rule_set_name, rule_set in self.rules.items():
            regras_dict = rule_set.get('regras', {})
            if isinstance(regras_dict, dict):
                for cat, regras in regras_dict.items():
                    if isinstance(regras, list):
                        total += len(regras)
        return total

    def load_rules(self, path):
        """Carrega regras de um arquivo YAML"""
        loader = RuleLoader(path)
        return loader.load()

    def evaluate(self, contexto: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Avalia regras para um contexto específico

        Args:
            contexto: dict com {modulo, metrics, data_id, ...}

        Returns:
            list: Ações executadas
        """
        print(f"🔍 Avaliando contexto: {contexto.get('modulo', 'unknown')}")

        acoes_executadas = []

        # Para cada arquivo de regras
        for rule_set_name, rule_set in self.rules.items():
            # Filtra regras relevantes
            relevant_rules = self.filter_relevant(rule_set, contexto)

            # Avalia cada regra
            for rule in relevant_rules:
                # Avalia condição
                try:
                    condition_met = self.parser.parse_and_eval(
                        rule["condicao"],
                        contexto
                    )

                    if condition_met:
                        # Executa ação
                        result = self.executor.execute(
                            rule["acao"],
                            rule,
                            contexto
                        )

                        # Logga
                        self.logger.log(rule, contexto, result)

                        # Coleta ação
                        acoes_executadas.append({
                            "rule_id": rule["id"],
                            "rule_set": rule_set_name,
                            "acao": rule["acao"],
                            "prioridade": rule.get("prioridade", "normal"),
                            "result": result
                        })

                        print(f"✅ {rule['id']}: {rule['acao']}")

                except Exception as e:
                    print(f"❌ Erro ao avaliar regra {rule['id']}: {e}")

        # Ordena por prioridade
        acoes_executadas.sort(key=lambda x: self.prioridade_score(x["prioridade"]))

        if acoes_executadas:
            print(f"🎯 {len(acoes_executadas)} ações executadas")

        return acoes_executadas

    def filter_relevant(self, rule_set: Dict[str, Any], contexto: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filtra regras relevantes para o contexto"""
        relevant = []

        categorias = rule_set.get("regras", {})

        for categoria, regras in categorias.items():
            for rule in regras:
                # Filtra por módulo
                if rule.get("modulo") == contexto.get("modulo"):
                    relevant.append(rule)
                elif rule.get("modulo") == "geral":
                    relevant.append(rule)

        return relevant

    def prioridade_score(self, prioridade: str) -> int:
        """Converte prioridade para score numérico"""
        scores = {
            "alta": 3,
            "normal": 2,
            "baixa": 1
        }
        return scores.get(prioridade, 2)

    def reload(self) -> Dict[str, int]:
        """Recarrega regras em runtime"""
        print("🔄 Recarregando regras...")
        self.load_all_rules()
        count = self.count_rules()
        print(f"✅ Regras recarregadas: {count}")
        return count

    def get_rules_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Busca regras por categoria"""
        rules = []

        for rule_set in self.rules.values():
            # rule_set["regras"] é um dict de categorias
            categorias = rule_set.get("regras", {})

            if category in categorias:
                rules.extend(categorias[category])

        return rules

    def get_rules_by_module(self, module: str) -> List[Dict[str, Any]]:
        """Busca regras por módulo"""
        rules = []

        for rule_set in self.rules.values():
            categorias = rule_set.get("regras", {})

            for categoria, regras in categorias.items():
                for rule in regras:
                    if rule.get("modulo") == module:
                        rules.append(rule)

        return rules


# Exemplo de uso
if __name__ == "__main__":
    # Inicia engine
    engine = RegrasEngine()

    # Contexto de exemplo
    contexto = {
        "modulo": "rastreador",
        "metrics": {
            "sources_collected": 10000,
            "max_sources": 10000
        },
        "data_id": "source_001"
    }

    # Avalia
    acoes = engine.evaluate(contexto)

    print(f"\n🎯 Ações executadas: {len(acoes)}")
    for acao in acoes:
        print(f"  - {acao['rule_id']}: {acao['acao']}")
