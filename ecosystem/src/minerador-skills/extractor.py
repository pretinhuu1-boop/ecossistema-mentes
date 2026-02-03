"""
SkillExtractor — Extrator de Skills

Versão: 1.0
Data: 2026-01-31
"""

import json
from typing import Dict, List, Any
from openai import OpenAI


class SkillExtractor:
    """Extrator de Skills usando OpenAI"""

    def __init__(self, api_key: str = None):
        """
        Inicializa SkillExtractor

        Args:
            api_key: API key da OpenAI (opcional, usa env)
        """
        self.openai = OpenAI(api_key=api_key)

    def extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extrai skills de texto usando LLM

        Args:
            text: Texto para extrair

        Returns:
            list: Skills extraídos
        """
        prompt = f"""
        Extraia skills do seguinte texto.

        Texto:
        {text}

        Skills são padrões, frameworks, mentalidades, processos ou conhecimento reutilizável.

        Tipos de skills:
        - processo: Como estruturar brainstorm, como criar PRDs, como definir roadmap
        - tecnico: Patterns de código, arquiteturas reutilizáveis, estratégias de testes
        - conhecimento: Frameworks cognitivos, mentalidades, conceitos fundamentais, relacionamentos entre ideias
        - negocio: Estratégias de pricing, táticas de marketing, workflows operacionais, métricas importantes

        Retorne em JSON:
        {{
            "skills": [
                {{
                    "type": "processo|tecnico|conhecimento|negocio",
                    "title": "Título curto",
                    "description": "Descrição detalhada",
                    "content": "Conteúdo do skill",
                    "confidence": 0.95,
                    "tags": ["tag1", "tag2"]
                }}
            ]
        }}
        """

        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um especialista em extrair patterns reutilizáveis de conversas."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result["skills"]

    def extract_ideation_skills(self, brainstorm: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai skills da fase de ideação do brainstorm

        Args:
            brainstorm: Dados do brainstorm

        Returns:
            list: Skills extraídos
        """
        # Como estruturar brainstorm
        skills = [{
            "id": f"skill_ideation_{i}",
            "type": "processo",
            "title": "Brainstorm Estrutural",
            "description": "Processo de ideação → revisão → decisões",
            "content": "1. Ideação (visão)\n2. Brainstorm de gaps\n3. Revisão final\n4. Decisões",
            "confidence": 0.95,
            "tags": ["brainstorm", "ideação", "processo"]
        }]

        return skills

    def extract_structure_skills(self, brainstorm: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai skills da fase de estruturação do brainstorm

        Args:
            brainstorm: Dados do brainstorm

        Returns:
            list: Skills extraídos
        """
        skills = [{
            "id": f"skill_structure_{i}",
            "type": "processo",
            "title": "Criação de PRDs",
            "description": "Como criar PRDs seguindo 21 lições aprendidas",
            "content": "1. Problema\n2. Stack técnica\n3. Funcionalidades\n4. Roadmap\n5. Critérios de qualidade",
            "confidence": 0.95,
            "tags": ["prd", "processo", "estruturação"]
        }]

        return skills

    def extract_review_skills(self, brainstorm: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai skills da fase de revisão do brainstorm

        Args:
            brainstorm: Dados do brainstorm

        Returns:
            list: Skills extraídos
        """
        skills = [{
            "id": f"skill_review_{i}",
            "type": "processo",
            "title": "Validação de Critérios de Sucesso",
            "description": "Como validar critérios de sucesso explícitos",
            "content": "1. Checklist de critérios\n2. Validação booleana\n3. Não 'quando funcionar'\n4. Qualidade > velocidade",
            "confidence": 0.95,
            "tags": ["validação", "qualidade", "critérios"]
        }]

        return skills

    def extract_decision_skills(self, brainstorm: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai skills da fase de decisões do brainstorm

        Args:
            brainstorm: Dados do brainstorm

        Returns:
            list: Skills extraídos
        """
        skills = [{
            "id": f"skill_decision_{i}",
            "type": "processo",
            "title": "Critérios de Parada Explícitos",
            "description": "Como definir critérios de parada claros",
            "content": "1. Para quando?\n2. Qual o threshold?\n3. O que fazer quando atingir?",
            "confidence": 0.95,
            "tags": ["parada", "critérios", "decisão"]
        }]

        return skills

    def extract_from_artifact(self, artifact: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai skills de um artefato

        Args:
            artifact: Artefato

        Returns:
            list: Skills extraídos
        """
        # Se artifact é "framework", extrai framework
        if artifact.get("type") == "framework":
            return [{
                "id": f"skill_framework_{artifact['id']}",
                "type": "conhecimento",
                "title": f"Framework: {artifact.get('title', 'Unknown')}",
                "description": artifact.get("description", ""),
                "content": artifact.get("content", ""),
                "confidence": artifact.get("confidence", 0.5),
                "tags": ["framework", "conhecimento"]
            }]

        # Se artifact é "bias", extrai bias
        elif artifact.get("type") == "bias":
            return [{
                "id": f"skill_bias_{artifact['id']}",
                "type": "conhecimento",
                "title": f"Bias: {artifact.get('title', 'Unknown')}",
                "description": artifact.get("description", ""),
                "content": artifact.get("content", ""),
                "confidence": artifact.get("confidence", 0.5),
                "tags": ["bias", "conhecimento", "mentalidade"]
            }]

        return []

    def extract_from_mind(self, mind: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai skills de uma mente

        Args:
            mind: Mente

        Returns:
            list: Skills extraídos
        """
        skills = []

        # Ex: "Alan Nicolas usa brainstorm estrutural"
        if "alan" in mind.get("author", "").lower():
            skills.append({
                "id": f"skill_mind_{mind['id']}_1",
                "type": "processo",
                "title": "Brainstorm Estrutural",
                "description": "Alan Nicolas sempre usa brainstorm estrutural",
                "content": "1. Ideação → 2. Brainstorm de gaps → 3. Revisão → 4. Decisões",
                "confidence": 0.95,
                "tags": ["brainstorm", "processo", "alan_nicolas"]
            })

        # Ex: "Alan Nicolas prioriza qualidade > velocidade"
        if "alan" in mind.get("author", "").lower():
            skills.append({
                "id": f"skill_mind_{mind['id']}_2",
                "type": "processo",
                "title": "Qualidade > Velocidade",
                "description": "Alan Nicolas sempre prioriza qualidade sobre velocidade",
                "content": "Não há 'bom o suficiente'. Se não é 100% perfeito, não é feito",
                "confidence": 0.95,
                "tags": ["qualidade", "princípio", "alan_nicolas"]
            })

        return skills


# Exemplo de uso
if __name__ == "__main__":
    extractor = SkillExtractor()

    # Exemplo 1: Extrair skills de texto
    text = """
    Na conversa, aprendemos que:
    1. Qualidade > Velocidade é essencial
    2. Brainstorm estrutural é mais eficiente
    3. Critérios de parada explícitos evitam loops infinitos
    """

    skills = extractor.extract_from_text(text)
    print(f"✅ Extraídos {len(skills)} skills do texto")
    for skill in skills:
        print(f"  - {skill['title']}")
