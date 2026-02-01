# MINERADOR DE SKILLS — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade CRÍTICA (GAP 20)
**Objetivo:** Minerar skills de conversas, brainstorms e dados minerados para reaproveitar conhecimento

---

## Problema

**Hoje:**
- Brainstorms são conversas únicas
- Conhecimento se perde após a conversa
- Skills descobertos em uma conversa não são reutilizados
- Dados minerados (artefatos, mentes) têm insights que não são capturados como skills

**Precisamos de:**
- Minerar skills de conversas passadas
- Minerar skills de brainstorms estruturais
- Minerar insights de dados minerados
- Criar biblioteca de skills reutilizáveis

---

## Stack Técnica

### Motor (Python)
- **Python** — Lógica de mineração
- **OpenAI API** — Extração de skills
- **SQLite** — Armazenamento de skills
- **ChromaDB** — Busca de skills (RAG)

### Integração
- **Sessions** → Minera conversas passadas
- **Orquestrador** → Dispara mineração após cada brainstorm
- **RAG** → Busca skills relevantes
- **RegrasEngine** → Regras de mineração de skills

---

## Funcionalidades

### Core
- [ ] Minerar skills de conversas
- [ ] Minerar skills de brainstorms estruturais
- [ ] Minerar insights de dados minerados
- [ ] Criar biblioteca de skills
- [ ] Buscar skills relevantes
- [ ] Sugerir skills para novos projetos

### Tipos de Skills

#### Skills de Processo
- Como estruturar brainstorm
- Como definir critérios de qualidade
- Como criar PRDs
- Como definir roadmap

#### Skills Técnicos
- Patterns de código
- Arquiteturas reutilizáveis
- Integrações comuns
- Estratégias de testes

#### Skills de Conhecimento
- Frameworks cognitivos
- Mentalidades
- Conceitos fundamentais
- Relacionamentos entre ideias

#### Skills de Negócio
- Estratégias de pricing
- Táticas de marketing
- Workflows operacionais
- Métricas importantes

---

## Minerador de Skills

```python
class SkillMiner:
    def __init__(self):
        self.openai = OpenAI()
        self.chroma = ChromaDB()
        self.skills_db = sqlite3.connect('skills.db')
        self.init_db()

    def init_db(self):
        """Inicializa banco de skills"""
        cursor = self.skills_db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                content TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_id TEXT,
                confidence REAL,
                created_at TEXT NOT NULL,
                tags TEXT,
                metadata TEXT
            )
        """)
        self.skills_db.commit()

    def mine_from_conversation(self, conversation_id):
        """
        Minera skills de uma conversa

        Args:
            conversation_id: ID da conversa (sessions history)

        Returns:
            list: Skills minerados
        """
        # Busca histórico da conversa
        history = self.get_conversation_history(conversation_id)

        # Extrai skills usando LLM
        skills = self.extract_skills_from_text(history)

        # Cria embeddings e salva
        saved_skills = []
        for skill in skills:
            # Cria embedding
            embedding = self.create_embedding(skill["content"])

            # Salva no banco
            skill_id = self.save_skill(skill, embedding)

            # Salva no ChromaDB
            self.chroma.add({
                "id": skill_id,
                "content": skill["content"],
                "metadata": {
                    "type": skill["type"],
                    "title": skill["title"],
                    "tags": skill.get("tags", [])
                }
            })

            saved_skills.append(skill_id)

        return saved_skills

    def mine_from_brainstorm(self, brainstorm_id):
        """
        Minera skills de um brainstorm estrutural

        Args:
            brainstorm_id: ID do brainstorm

        Returns:
            list: Skills minerados
        """
        # Busca brainstorm
        brainstorm = self.get_brainstorm(brainstorm_id)

        # Extrai skills de cada fase do brainstorm
        skills = []

        # Fase 1: Ideação
        skills += self.extract_ideation_skills(brainstorm)

        # Fase 2: Estruturação
        skills += self.extract_structure_skills(brainstorm)

        # Fase 3: Revisão
        skills += self.extract_review_skills(brainstorm)

        # Fase 4: Decisões
        skills += self.extract_decision_skills(brainstorm)

        # Salva
        saved_skills = []
        for skill in skills:
            skill_id = self.save_skill(skill)
            saved_skills.append(skill_id)

        return saved_skills

    def mine_from_mined_data(self, project_id):
        """
        Minera skills de dados já minerados

        Args:
            project_id: ID do projeto

        Returns:
            list: Skills minerados
        """
        # Busca dados minerados
        artifacts = ArtifactStore.get_by_project(project_id)
        minds = MindStore.get_by_project(project_id)

        # Extrai skills de artefatos
        skills = []
        for artifact in artifacts:
            skills += self.extract_skills_from_artifact(artifact)

        # Extrai skills de mentes
        for mind in minds:
            skills += self.extract_skills_from_mind(mind)

        # Salva
        saved_skills = []
        for skill in skills:
            skill_id = self.save_skill(skill)
            saved_skills.append(skill_id)

        return saved_skills

    def extract_skills_from_text(self, text):
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

    def extract_ideation_skills(self, brainstorm):
        """Extrai skills da fase de ideação"""
        # Como estruturar brainstorm
        # Como identificar gaps
        # Como definir objetivos
        pass

    def extract_structure_skills(self, brainstorm):
        """Extrai skills da fase de estruturação"""
        # Como criar PRDs
        # Como definir roadmap
        # Como criar arquiteturas
        pass

    def extract_review_skills(self, brainstorm):
        """Extrai skills da fase de revisão"""
        # Como validar PRDs
        # Como fazer code review
        # Como identificar problemas
        pass

    def extract_decision_skills(self, brainstorm):
        """Extrai skills da fase de decisões"""
        # Como tomar decisões técnicas
        # Como tradeoff features
        # Como priorizar
        pass

    def extract_skills_from_artifact(self, artifact):
        """Extrai skills de um artefato"""
        # Se artifact é "framework", extrai framework
        # Se artifact é "bias", extrai bias
        pass

    def extract_skills_from_mind(self, mind):
        """Extrai skills de uma mente"""
        # Ex: "Alan Nicolas usa brainstorm estrutural"
        # Ex: "Alan Nicolas prioriza qualidade > velocidade"
        pass

    def create_embedding(self, content):
        """Cria embedding de skill"""
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=content
        )
        return response.data[0].embedding

    def save_skill(self, skill, embedding=None):
        """Salva skill no banco"""
        cursor = self.skills_db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO skills (id, type, title, description, content,
                                          source_type, source_id, confidence, created_at, tags, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            skill.get("id", str(uuid4())),
            skill["type"],
            skill["title"],
            skill.get("description", ""),
            skill["content"],
            skill.get("source_type", "unknown"),
            skill.get("source_id", ""),
            skill.get("confidence", 0.5),
            datetime.now().isoformat(),
            json.dumps(skill.get("tags", [])),
            json.dumps(skill.get("metadata", {}))
        ))
        self.skills_db.commit()
        return skill.get("id", str(uuid4()))

    def search_skills(self, query, top_k=10):
        """
        Busca skills relevantes

        Args:
            query: Query de busca
            top_k: Número de resultados

        Returns:
            list: Skills relevantes
        """
        # Cria embedding da query
        query_embedding = self.create_embedding(query)

        # Busca no ChromaDB
        results = self.chroma.query(
            query_vector=query_embedding,
            n_results=top_k
        )

        # Formata resultados
        skills = []
        for result in results:
            skill = self.get_skill(result["id"])
            skills.append(skill)

        return skills

    def suggest_skills(self, project_description):
        """
        Sugere skills para um novo projeto

        Args:
            project_description: Descrição do projeto

        Returns:
            list: Skills sugeridos
        """
        # Extrai palavras-chave da descrição
        keywords = self.extract_keywords(project_description)

        # Busca skills por tags
        skills = []
        for keyword in keywords:
            skills += self.search_skills(f"tag:{keyword}")

        # Deduplica
        skills = list({s["id"]: s for s in skills}.values())

        return skills

    def extract_keywords(self, text):
        """Extrai palavras-chave"""
        # Simplificação: split por espaço
        # Na prática, usaria NLP
        return text.split()[:10]
```

---

## Integração com Sessions

### Mineração Automática de Conversas
```python
@subscriber(EventType.SESSION_COMPLETED)
def on_session_completed(event_data):
    """Quando uma conversa termina, minera skills"""
    session_id = event_data["session_id"]

    # Minera skills
    miner = SkillMiner()
    skills = miner.mine_from_conversation(session_id)

    print(f"✅ Minerei {len(skills)} skills da conversa {session_id}")
```

---

## Integração com Orquestrador

### Mineração de Brainstorms
```python
def after_brainstorm(project_name, brainstorm_id):
    """Após brainstorm, minera skills"""
    miner = SkillMiner()
    skills = miner.mine_from_brainstorm(brainstorm_id)

    print(f"✅ Minerei {len(skills)} skills do brainstorm {brainstorm_id}")
```

---

## Integração com Orquestrador

### Mineração de Dados Minerados
```python
def after_mining(project_id):
    """Após mineração de dados, minera skills"""
    miner = SkillMiner()
    skills = miner.mine_from_mined_data(project_id)

    print(f"✅ Minerei {len(skills)} skills dos dados minerados do projeto {project_id}")
```

---

## Integração com Clawdbot

### Command: `skills suggest`
```bash
# Sugerir skills para um novo projeto
skills suggest --project "Criar ecossistema de mentes"

# Buscar skills
skills search --query "brainstorm estrutural"

# Listar skills por tipo
skills list --type processo

# Ver skill específico
skills get --id skill_001

# Minerar skills de conversa
skills mine --conversation session_123

# Minerar skills de brainstorm
skills mine --brainstorm brainstorm_456
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Minerador de Skills básico
- [ ] Mineração de conversas
- [ ] Busca de skills
- [ ] Biblioteca de skills

### v0.5
- [ ] Mineração de brainstorms
- [ ] Mineração de dados minerados
- [ ] Sugestão de skills
- [ ] Tags de skills

### v1.0
- [ ] Integração com Sessions (auto-mineração)
- [ ] Integração com Orquestrador
- [ ] Dashboard de skills
- [ ] Skills versionados

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 20*
