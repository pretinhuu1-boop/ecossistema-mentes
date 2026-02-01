#!/usr/bin/env python3
"""
Teste Standalone do RegrasEngine

Versão: 1.0
Data: 2026-01-31
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from regras.engine import RegrasEngine


def test_engine():
    """Testa RegrasEngine"""
    print("=" * 60)
    print("🧪 TESTE REGRASENGINE")
    print("=" * 60)

    # Teste 1: Inicializar engine
    print("\n1️⃣ Inicializando RegrasEngine...")
    try:
        engine = RegrasEngine(rules_dir="rules")
        print("   ✅ Engine inicializado com sucesso")
    except Exception as e:
        print(f"   ❌ Erro ao inicializar: {e}")
        return False

    # Teste 2: Contar regras
    print("\n2️⃣ Contando regras carregadas...")
    total = engine.count_rules()
    print(f"   ✅ Total de regras: {total}")
    if total == 0:
        print("   ⚠️ Nenhuma regra carregada!")
        return False

    # Teste 3: Buscar regras por categoria
    print("\n3️⃣ Buscando regras por categoria...")
    for categoria in ["operacao", "qualidade", "decisao"]:
        rules = engine.get_rules_by_category(categoria)
        print(f"   ✅ Categoria '{categoria}': {len(rules)} regras")

    # Teste 4: Buscar regras por módulo
    print("\n4️⃣ Buscando regras por módulo...")
    for modulo in ["rastreador", "minerador", "loop"]:
        rules = engine.get_rules_by_module(modulo)
        print(f"   ✅ Módulo '{modulo}': {len(rules)} regras")

    # Teste 5: Avaliar contexto (R-OP-01)
    print("\n5️⃣ Testando regra R-OP-01 (sources_collected >= max_sources)...")
    contexto1 = {
        "modulo": "rastreador",
        "sources_collected": 10000,
        "max_sources": 10000,
        "data_id": "source_001"
    }

    acoes1 = engine.evaluate(contexto1)
    print(f"   ✅ {len(acoes1)} ações executadas")
    for acao in acoes1:
        print(f"      - {acao['rule_id']}: {acao['acao']}")

    # Teste 6: Avaliar contexto (R-OP-06)
    print("\n6️⃣ Testando regra R-OP-06 (confidence_mean < 0.7)...")
    contexto2 = {
        "modulo": "minerador",
        "confidence_mean": 0.65,
        "min_confidence_mean": 0.7,
        "data_id": "artifact_001"
    }

    acoes2 = engine.evaluate(contexto2)
    print(f"   ✅ {len(acoes2)} ações executadas")
    for acao in acoes2:
        print(f"      - {acao['rule_id']}: {acao['acao']}")

    # Teste 7: Avaliar contexto (Loop)
    print("\n7️⃣ Testando regra R-OP-09 (iteration >= 10)...")
    contexto3 = {
        "modulo": "loop",
        "iteration": 10,
        "max_iterations": 10,
        "data_id": "loop_001"
    }

    acoes3 = engine.evaluate(contexto3)
    print(f"   ✅ {len(acoes3)} ações executadas")
    for acao in acoes3:
        print(f"      - {acao['rule_id']}: {acao['acao']}")

    # Teste 8: Reload
    print("\n8️⃣ Testando reload de regras...")
    try:
        count = engine.reload()
        print(f"   ✅ Regras recarregadas: {count}")
    except Exception as e:
        print(f"   ❌ Erro ao recarregar: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_engine()
    sys.exit(0 if success else 1)
