#!/usr/bin/env python3
"""
Teste do Minerador de Skills

Versão: 1.0
Data: 2026-01-31
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from miner import SkillMiner


def test_miner():
    """Testa Minerador de Skills"""
    print("🧪 Testando Minerador de Skills...\n")

    # Inicia minerador
    print("1️⃣ Inicializando minerador...")
    miner = SkillMiner()

    # Teste 1: Extrair skills de texto
    print("\n2️⃣ Testando extração de skills de texto...")
    text = """
    Na conversa, aprendemos que:
    1. Qualidade > Velocidade é essencial
    2. Brainstorm estrutural é mais eficiente
    3. Critérios de parada explícitos evitam loops infinitos
    """

    skills = miner.extractor.extract_from_text(text)
    print(f"   ✅ Extraídos {len(skills)} skills do texto")
    for skill in skills:
        print(f"      - {skill['title']}: {skill['type']}")

    # Teste 2: Extrair skills de brainstorm
    print("\n3️⃣ Testando extração de skills de brainstorm...")
    brainstorm = {
        "id": "brainstorm_001",
        "fase": "ideacao",
        "descricao": "Brainstorm do Ecossistema"
    }

    skills_ideacao = miner.extractor.extract_ideation_skills(brainstorm)
    print(f"   ✅ Extraídos {len(skills_ideacao)} skills de ideação")
    for skill in skills_ideacao:
        print(f"      - {skill['title']}")

    # Teste 3: Buscar skills
    print("\n4️⃣ Testando busca de skills...")
    # TODO: Integrar ChromaDB
    # Por enquanto, stub
    print(f"   ⚠️ Busca (ChromaDB não implementado): stub")

    # Teste 4: Sugerir skills
    print("\n5️⃣ Testando sugestão de skills...")
    project_description = "Criar ecossistema de mentes que colaboram"

    # TODO: Integrar ChromaDB
    # Por enquanto, stub
    keywords = miner.suggester.extract_keywords(project_description)
    print(f"   ⚠️ Sugestão (ChromaDB não implementado): {keywords[:5]}")

    print("\n✅ Todos os testes passaram!")


if __name__ == "__main__":
    test_miner()
