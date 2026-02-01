"""
SkillSuggester — Sugestão de Skills

Versão: 1.0
Data: 2026-01-31
"""

from typing import Dict, List, Any
from .search import SkillSearch


class SkillSuggester:
    """Sugestor de Skills para novos projetos"""

    def __init__(self, chroma_host: str = "localhost", chroma_port: int = 8000):
        """
        Inicializa SkillSuggester

        Args:
            chroma_host: Host do ChromaDB
            chroma_port: Porta do ChromaDB
        """
        self.search = SkillSearch(chroma_host, chroma_port)

    def suggest(self, project_description: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Sugere skills para um novo projeto

        Args:
            project_description: Descrição do projeto
            top_k: Número de sugestões

        Returns:
            list: Skills sugeridos
        """
        print(f"💡 Sugerindo skills para: {project_description}")

        # Extrai palavras-chave da descrição
        keywords = self.extract_keywords(project_description)

        print(f"   Palavras-chave: {keywords}")

        # Busca skills por tags
        skills = []
        for keyword in keywords:
            query = f"tag:{keyword}"
            results = self.search.search(query, top_k=5)
            skills.extend(results)

        # Deduplica
        skills = list({s.get("id", ""): s for s in skills}.values())

        # Limita
        skills = skills[:top_k]

        print(f"✅ Sugeridos {len(skills)} skills")

        return skills

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extrai palavras-chave

        Args:
            text: Texto para extrair

        Returns:
            list: Palavras-chave
        """
        # Simplificação: split por espaço
        # Remove stopwords
        stopwords = ["de", "para", "o", "a", "em", "com", "do", "da", "um", "uma", "e", "ou"]

        words = text.lower().split()
        keywords = [w for w in words if w not in stopwords and len(w) > 3]

        return keywords[:10]


# Exemplo de uso
if __name__ == "__main__":
    suggester = SkillSuggester()

    # Exemplo: Sugere skills para um projeto
    project_description = "Criar ecossistema de mentes que colaboram entre si"

    skills = suggester.suggest(project_description)

    print(f"\nSugestões:")
    for i, skill in enumerate(skills):
        print(f"  {i+1}. {skill.get('title', 'Unknown')}")
