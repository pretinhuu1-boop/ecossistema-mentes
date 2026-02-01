#!/usr/bin/env python3
"""
Teste do RegrasEngine

Versão: 1.0
Data: 2026-01-31
"""

import sys
import os

# Adiciona src/regras ao path
regras_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, regras_dir)

# Importa sem relative imports
from loader import RuleLoader


def test_loader():
    """Testa RuleLoader"""
    print("🧪 Testando RuleLoader...\n")

    # Inicia loader
    print("1️⃣ Inicializando loader...")
    loader = RuleLoader("../../rules/ecossistema.yaml")

    # Carrega regras
    print("\n2️⃣ Carregando regras...")
    data = loader.load()

    print(f"   ✅ {len(data.get('regras', []))} regras carregadas")

    # Mostra primeiras regras
    print("\n3️⃣ Mostrando primeiras regras...")
    for i, rule in enumerate(data.get("regras", [])[:5]):
        print(f"   {i+1}. {rule['id']}: {rule['acao']}")

    print("\n✅ Teste passou!")


if __name__ == "__main__":
    test_loader()
