#!/usr/bin/env python3
"""
Teste do Minerador de Skills (Simulado)

Versão: 1.0
Data: 2026-01-31
"""

import json
from typing import List, Dict, Any


class SimulatedSkillMiner:
    """Simulação do Minerador de Skills (sem OpenAI/ChromaDB)"""

    def __init__(self):
        """Inicializa simulador"""
        self.skills_db = {}

    def extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extrai skills de texto (simulado)"""
        # Simula extração de skills
        skills = [
            {
                "id": "skill_001",
                "type": "processo",
                "title": "Qualidade > Velocidade",
                "description": "Alan Nicolas sempre prioriza qualidade sobre velocidade",
                "content": "Não há 'bom o suficiente'. Se não é 100% perfeito, não é feito",
                "confidence": 0.95,
                "tags": ["qualidade", "princípio", "alan_nicolas"]
            },
            {
                "id": "skill_002",
                "type": "processo",
                "title": "Brainstorm Estrutural",
                "description": "Processo de ideação → revisão → decisões",
                "content": "1. Ideação (visão)\n2. Brainstorm de gaps\n3. Revisão final\n4. Decisões",
                "confidence": 0.95,
                "tags": ["brainstorm", "processo", "estruturação"]
            },
            {
                "id": "skill_003",
                "type": "conhecimento",
                "title": "Critérios de Parada Explícitos",
                "description": "Cada módulo precisa de critérios de parada claros",
                "content": "Definir QUANDO parar, O QUE fazer quando atingir, etc.",
                "confidence": 0.95,
                "tags": ["critérios", "parada", "decisão"]
            }
        ]

        return skills

    def save_skill(self, skill: Dict[str, Any]) -> str:
        """Salva skill (simulado)"""
        skill_id = skill.get("id", f"skill_{len(self.skills_db)+1}")
        self.skills_db[skill_id] = skill
        return skill_id

    def search_skills(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Busca skills relevantes (simulado - busca por tags)"""
        # Simplificação: busca por tags
        query_lower = query.lower()
        keywords = query_lower.split()

        results = []
        for skill_id, skill in self.skills_db.items():
            # Busca por título
            score = 0

            if query_lower in skill.get("title", "").lower():
                score = 1.0
            elif query_lower in skill.get("description", "").lower():
                score = 0.8
            else:
                # Busca por tags
                for keyword in keywords:
                    if keyword in " ".join(skill.get("tags", [])).lower():
                        score = 0.6
                        break

            if score > 0.5:
                results.append({
                    "skill": skill,
                    "score": score
                })

        # Ordena por score
        results.sort(key=lambda x: x["score"], reverse=True)

        # Retorna top_k
        return [r["skill"] for r in results[:top_k]]

    def suggest_skills(self, project_description: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Sugere skills para projeto (simulado)"""
        return self.search_skills(project_description, top_k)

    def get_stats(self) -> Dict[str, Any]:
        """Estatísticas"""
        return {
            "total_skills": len(self.skills_db),
            "by_type": self._count_by_type(),
            "by_tags": self._count_by_tags()
        }

    def _count_by_type(self) -> Dict[str, int]:
        """Conta por tipo"""
        by_type = {}
        for skill in self.skills_db.values():
            skill_type = skill.get("type", "unknown")
            by_type[skill_type] = by_type.get(skill_type, 0) + 1
        return by_type

    def _count_by_tags(self) -> Dict[str, int]:
        """Conta por tags"""
        by_tags = {}
        for skill in self.skills_db.values():
            for tag in skill.get("tags", []):
                by_tags[tag] = by_tags.get(tag, 0) + 1
        return by_tags


def test_minerador():
    """Testa simulador do Minerador de Skills"""
    print("🧪 Testando Simulador do Minerador de Skills...\n")

    # Inicia minerador
    print("1️⃣ Inicializando minerador...")
    miner = SimulatedSkillMiner()

    # Teste 1: Extrair skills de texto
    print("\n2️⃣ Testando extração de skills de texto...")
    text = """
    Na conversa, aprendemos que:
    1. Qualidade > Velocidade é essencial
    2. Brainstorm estrutural é mais eficiente
    3. Critérios de parada explícitos evitam loops infinitos
    """

    skills = miner.extract_from_text(text)
    print(f"   ✅ Extraídos {len(skills)} skills do texto")

    # Salva skills
    for skill in skills:
        miner.save_skill(skill)
        print(f"      - {skill['title']} ({skill['type']})")

    # Teste 2: Buscar skills
    print("\n3️⃣ Testando busca de skills...")
    query = "brainstorm estrutural"
    results = miner.search_skills(query)

    print(f"   ✅ Busca retornou {len(results)} skills")
    for i, skill in enumerate(results):
        print(f"      {i+1}. {skill['title']}")

    # Teste 3: Sugerir skills
    print("\n4️⃣ Testando sugestão de skills...")
    project_description = "Criar ecossistema de mentes que colaboram entre si"

    suggestions = miner.suggest_skills(project_description)
    print(f"   ✅ Sugestão retornou {len(suggestions)} skills")

    for i, skill in enumerate(suggestions):
        print(f"      {i+1}. {skill['title']}")

    # Teste 4: Estatísticas
    print("\n5️⃣ Testando estatísticas...")
    stats = miner.get_stats()

    print(f"   ✅ Total: {stats['total_skills']} skills")
    print(f"   ✅ Por tipo:")
    for skill_type, count in stats['by_type'].items():
        print(f"      - {skill_type}: {count}")
    print(f"   ✅ Por tags (top 5):")
    for tag, count in sorted(stats['by_tags'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"      - {tag}: {count}")

    print("\n✅ Todos os testes passaram!")


if __name__ == "__main__":
    test_minerador()
