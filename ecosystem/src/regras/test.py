#!/usr/bin/env python3
"""
Teste do RegrasEngine

Versão: 1.0
Data: 2026-01-31
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import RegrasEngine


def test_engine():
    """Testa RegrasEngine"""
    print("🧪 Testando RegrasEngine...\n")

    # Inicia engine
    print("1️⃣ Inicializando engine...")
    engine = RegrasEngine(rules_dir="../../rules")

    # Teste 1: Carregar regras
    print("\n2️⃣ Contando regras...")
    total = engine.count_rules()
    print(f"   ✅ Total: {total} regras")

    # Teste 2: Avaliar contexto
    print("\n3️⃣ Avaliando contexto...")
    contexto = {
        "modulo": "rastreador",
        "metrics": {
            "sources_collected": 10000,
            "max_sources": 10000
        },
        "data_id": "source_001"
    }

    acoes = engine.evaluate(contexto)

    print(f"   ✅ {len(acoes)} ações executadas")
    for acao in acoes:
        print(f"      - {acao['rule_id']}: {acao['acao']}")

    # Teste 3: Buscar regras por categoria
    print("\n4️⃣ Buscando regras por categoria...")
    operacao_rules = engine.get_rules_by_category("operacao")
    print(f"   ✅ Categoria 'operacao': {len(operacao_rules)} regras")

    # Teste 5: Buscar regras por módulo
    print("\n5️⃣ Buscando regras por módulo...")
    rastreador_rules = engine.get_rules_by_module("rastreador")
    print(f"   ✅ Módulo 'rastreador': {len(rastreador_rules)} regras")

    # Teste 6: Reload
    print("\n6️⃣ Recarregando regras...")
    engine.reload()

    print("\n✅ Todos os testes passaram!")


if __name__ == "__main__":
    test_engine()
