"""
SkillMiner — Minerador de Skills

Versão: 1.0
Data: 2026-01-31
"""

import os
from typing import Dict, List, Any

from .extractor import SkillExtractor
from .search import SkillSearch
from .suggester import SkillSuggester


class SkillMiner:
    """Minerador de Skills de conversas, brainstorms e dados minerados"""

    def __init__(self):
        """Inicializa SkillMiner"""
        self.extractor = SkillExtractor()
        self.search = SkillSearch()
        self.suggester = SkillSuggester()

    def mine_from_conversation(self, conversation_id: str) -> List[str]:
        """
        Minera skills de uma conversa

        Args:
            conversation_id: ID da conversa (sessions history)

        Returns:
            list: IDs dos skills minerados
        """
        print(f"📥 Minerando skills da conversa {conversation_id}...")

        # Busca histórico da conversa
        history = self.get_conversation_history(conversation_id)

        if not history:
            print(f"⚠️ Histórico não encontrado: {conversation_id}")
            return []

        # Extrai skills usando LLM
        skills = self.extractor.extract_from_text(history)

        # Salva skills
        saved_skill_ids = []
        for skill in skills:
            skill_id = self.save_skill(skill)
            saved_skill_ids.append(skill_id)

        print(f"✅ Minerados {len(saved_skill_ids)} skills da conversa")

        return saved_skill_ids

    def mine_from_brainstorm(self, brainstorm_id: str) -> List[str]:
        """
        Minera skills de um brainstorm estrutural

        Args:
            brainstorm_id: ID do brainstorm

        Returns:
            list: IDs dos skills minerados
        """
        print(f"🧩 Minerando skills do brainstorm {brainstorm_id}...")

        # Busca brainstorm
        brainstorm = self.get_brainstorm(brainstorm_id)

        if not brainstorm:
            print(f"⚠️ Brainstorm não encontrado: {brainstorm_id}")
            return []

        # Extrai skills de cada fase do brainstorm
        skills = []

        # Fase 1: Ideação
        skills += self.extractor.extract_ideation_skills(brainstorm)

        # Fase 2: Estruturação
        skills += self.extractor.extract_structure_skills(brainstorm)

        # Fase 3: Revisão
        skills += self.extractor.extract_review_skills(brainstorm)

        # Fase 4: Decisões
        skills += self.extractor.extract_decision_skills(brainstorm)

        # Salva skills
        saved_skill_ids = []
        for skill in skills:
            skill_id = self.save_skill(skill)
            saved_skill_ids.append(skill_id)

        print(f"✅ Minerados {len(saved_skill_ids)} skills do brainstorm")

        return saved_skill_ids

    def mine_from_mined_data(self, project_id: str) -> List[str]:
        """
        Minera skills de dados já minerados

        Args:
            project_id: ID do projeto

        Returns:
            list: IDs dos skills minerados
        """
        print(f"📦 Minerando skills dos dados minerados do projeto {project_id}...")

        # Busca dados minerados
        artifacts = self.get_project_artifacts(project_id)
        minds = self.get_project_minds(project_id)

        # Extrai skills de artefatos
        skills = []
        for artifact in artifacts:
            skills += self.extractor.extract_from_artifact(artifact)

        # Extrai skills de mentes
        for mind in minds:
            skills += self.extractor.extract_from_mind(mind)

        # Salva skills
        saved_skill_ids = []
        for skill in skills:
            skill_id = self.save_skill(skill)
            saved_skill_ids.append(skill_id)

        print(f"✅ Minerados {len(saved_skill_ids)} skills dos dados minerados")

        return saved_skill_ids

    def search_skills(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Busca skills relevantes

        Args:
            query: Query de busca
            top_k: Número de resultados

        Returns:
            list: Skills relevantes
        """
        print(f"🔍 Buscando skills: {query}")

        # Busca skills
        skills = self.search.search(query, top_k)

        print(f"✅ Encontrados {len(skills)} skills")

        return skills

    def suggest_skills(self, project_description: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Sugere skills para um novo projeto

        Args:
            project_description: Descrição do projeto
            top_k: Número de sugestões

        Returns:
            list: Skills sugeridos
        """
        print(f"💡 Sugerindo skills para: {project_description}")

        # Sugere skills
        skills = self.suggester.suggest(project_description, top_k)

        print(f"✅ Sugeridos {len(skills)} skills")

        return skills

    def get_conversation_history(self, conversation_id: str) -> str:
        """Busca histórico da conversa (stub)"""
        # TODO: Integrar com Sessions
        # Por enquanto, retorna vazio
        return ""

    def get_brainstorm(self, brainstorm_id: str) -> Dict[str, Any]:
        """Busca brainstorm (stub)"""
        # TODO: Integrar com Orquestrador
        # Por enquanto, retorna vazio
        return {}

    def get_project_artifacts(self, project_id: str) -> List[Dict[str, Any]]:
        """Busca artefatos do projeto (stub)"""
        # TODO: Integrar com Estado Persistente
        # Por enquanto, retorna vazio
        return []

    def get_project_minds(self, project_id: str) -> List[Dict[str, Any]]:
        """Busca mentes do projeto (stub)"""
        # TODO: Integrar com Biblioteca de Mentes
        # Por enquanto, retorna vazio
        return []

    def save_skill(self, skill: Dict[str, Any]) -> str:
        """Salva skill (stub)"""
        # TODO: Salvar em banco skills.db
        # TODO: Criar embedding e salvar no ChromaDB
        skill_id = skill.get("id", f"skill_{os.urandom(8).hex()}")
        return skill_id


# Exemplo de uso
if __name__ == "__main__":
    miner = SkillMiner()

    # Exemplo 1: Minera skills de conversa
    skills = miner.mine_from_conversation("session_123")
    print(f"\nSkills minerados: {len(skills)}")

    # Exemplo 2: Busca skills
    results = miner.search_skills("brainstorm estrutural")
    print(f"\nBusca retornou: {len(results)} skills")
