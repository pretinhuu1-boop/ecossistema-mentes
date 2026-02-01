# SQUADS — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Média (GAP 7)

---

## Problema

**Hoje:**
- "Squad toma decisões"
- **Mas QUAL mecanismo de tomada de decisão?**

**Precisamos de:**
- Framework de tomada de decisão
- Múltiplos frameworks disponíveis
- Configurável por squad

---

## Stack Técnica

### Motor (Python)
- **LangChain** — Orquestração de agents
- **OpenAI API** — Decisões
- **Python** — Lógica de frameworks

### Integração
- **Biblioteca de Mentes** — Fornece mentes para squads
- **RAG** — Busca decisões similares anteriores
- **Orquestrador** — Coordena squads

---

## Funcionalidades

### Core
- [ ] Framework de tomada de decisão
- [ ] Múltiplos frameworks (consensus, weighted, expert, delegation)
- [ ] Configurável por squad
- [ ] Histórico de decisões

### Frameworks
- [ ] **Consensus** — Todos concordam
- [ ] **Weighted Vote** — Voto ponderado por expertise
- [ ] **Expert-Based** — Especialista naquele tema decide
- [ ] **Delegation** — Delega pra outro squad

### Learning
- [ ] Aprende com decisões anteriores
- [ ] Melhora frameworks ao longo do tempo
- [ ] Detecta padrões de decisão

---

## Framework de Tomada de Decisão

```python
class SquadDecisionFramework:
    def __init__(self, framework_type="weighted_vote"):
        self.framework_type = framework_type
        self.openai = OpenAI()
        self.decision_history = DecisionHistory()

    def decide(self, context, squad):
        """
        Toma decisão baseada no framework

        Args:
            context: Contexto da decisão
            squad: Squad (lista de agents/mentes)

        Returns:
            dict: Decisão tomada
        """
        # Se framework requer, busca decisões anteriores
        if self.framework_type in ["weighted_vote", "expert_based"]:
            previous_decisions = self.decision_history.search(context)
        else:
            previous_decisions = None

        # Escolhe framework e decide
        if self.framework_type == "consensus":
            return self.consensus(context, squad)
        elif self.framework_type == "weighted_vote":
            return self.weighted_vote(context, squad, previous_decisions)
        elif self.framework_type == "expert_based":
            return self.expert_based(context, squad, previous_decisions)
        elif self.framework_type == "delegation":
            return self.delegation(context, squad, previous_decisions)
        else:
            raise ValueError(f"Framework desconhecido: {self.framework_type}")

    def consensus(self, context, squad):
        """
        Framework: Consensus

        Todos os agents devem concordar.
        """
        # Coleta opiniões de todos
        opinions = []
        for agent in squad:
            opinion = agent.get_opinion(context)
            opinions.append({
                "agent_id": agent.id,
                "opinion": opinion
            })

        # Verifica se há consenso
        all_agree = all(o["opinion"] == opinions[0]["opinion"] for o in opinions)

        if all_agree:
            # Consenso!
            decision = {
                "decision": opinions[0]["opinion"],
                "framework": "consensus",
                "unanimous": True,
                "votes": opinions,
                "confidence": 1.0
            }
        else:
            # Sem consenso → negociação
            decision = self.negotiate(context, opinions)

        # Salva no histórico
        self.decision_history.save(decision, context)

        return decision

    def weighted_vote(self, context, squad, previous_decisions):
        """
        Framework: Weighted Vote

        Voto ponderado por expertise.
        """
        # Coleta pesos de expertise
        weights = self.calculate_expertise_weights(squad, context, previous_decisions)

        # Coleta votos
        votes = []
        for agent, weight in zip(squad, weights):
            vote = agent.get_vote(context)
            votes.append({
                "agent_id": agent.id,
                "vote": vote,
                "weight": weight
            })

        # Calcula resultado ponderado
        # Se votos são numéricos, weighted average
        # Se votos são opções, weighted voting
        if isinstance(votes[0]["vote"], (int, float)):
            # Weighted average
            result = sum(v["vote"] * v["weight"] for v in votes) / sum(weights)
        else:
            # Weighted voting
            vote_counts = defaultdict(float)
            for vote in votes:
                vote_counts[vote["vote"]] += vote["weight"]

            result = max(vote_counts.items(), key=lambda x: x[1])[0]

        # Calcula confiança
        confidence = self.calculate_vote_confidence(votes, weights)

        decision = {
            "decision": result,
            "framework": "weighted_vote",
            "unanimous": False,
            "votes": votes,
            "confidence": confidence
        }

        # Salva no histórico
        self.decision_history.save(decision, context)

        return decision

    def expert_based(self, context, squad, previous_decisions):
        """
        Framework: Expert-Based

        Especialista naquele tema decide.
        """
        # Identifica especialista
        expert = self.identify_expert(context, squad, previous_decisions)

        # Especialista decide
        decision = expert.decide(context)

        decision = {
            "decision": decision,
            "framework": "expert_based",
            "unanimous": False,
            "expert_id": expert.id,
            "votes": [{
                "agent_id": expert.id,
                "vote": decision,
                "weight": 1.0
            }],
            "confidence": expert.confidence(context)
        }

        # Salva no histórico
        self.decision_history.save(decision, context)

        return decision

    def delegation(self, context, squad, previous_decisions):
        """
        Framework: Delegation

        Delega pra outro squad.
        """
        # Identifica qual squad deve delegar
        target_squad = self.identify_target_squad(context, squad, previous_decisions)

        # Delega
        delegated_decision = target_squad.decide(context)

        decision = {
            "decision": delegated_decision["decision"],
            "framework": "delegation",
            "unanimous": False,
            "delegated_to": target_squad.id,
            "original_squad": squad.id,
            "votes": [],
            "confidence": delegated_decision["confidence"] * 0.9  # Pequena penalidade por delegação
        }

        # Salva no histórico
        self.decision_history.save(decision, context)

        return decision

    def negotiate(self, context, opinions):
        """
        Negocia quando não há consenso
        """
        # Usa LLM pra negociar
        prompt = f"""
Negocie uma decisão entre estas opiniões:

CONTEXTO: {context}

OPINIÕES:
{opinions}

Retorne:
- decision: A decisão final
- consensus: Se houve consenso (True/False)
- notes: Notas sobre a negociação
"""

        response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        negotiation = parse_negotiation(response.choices[0].message.content)

        return {
            "decision": negotiation["decision"],
            "framework": "consensus",
            "unanimous": negotiation["consensus"],
            "votes": opinions,
            "confidence": 0.8,  # Consenso após negociação é menos confiável que unanimidade
            "notes": negotiation["notes"]
        }

    def calculate_expertise_weights(self, squad, context, previous_decisions):
        """Calcula pesos de expertise baseado em decisões anteriores"""
        weights = []

        for agent in squad:
            # Se há decisões anteriores similares
            if previous_decisions:
                # Calcula expertise baseado em sucesso
                expertise = self.calculate_expertise_from_history(agent, context, previous_decisions)
            else:
                # Se não, usa expertise base do agent
                expertise = agent.expertise(context)

            weights.append(expertise)

        # Normaliza pra somar 1
        total = sum(weights)
        weights = [w / total for w in weights]

        return weights

    def identify_expert(self, context, squad, previous_decisions):
        """Identifica especialista no contexto"""
        # Calcula expertise de cada agent
        expertise_scores = [
            self.calculate_expertise(agent, context, previous_decisions)
            for agent in squad
        ]

        # Retorna o com maior expertise
        return squad[expertise_scores.index(max(expertise_scores))]

    def calculate_expertise(self, agent, context, previous_decisions):
        """Calcula expertise de um agent em um contexto"""
        # Simplificação: usa expertise base do agent
        # TODO: Implementar cálculo real baseado em histórico
        return agent.expertise(context)

    def identify_target_squad(self, context, squad, previous_decisions):
        """Identifica qual squad deve receber delegação"""
        # Simplificação: usa regra hard-coded
        # Data Squad → Strategy Squad, etc.
        # TODO: Implementar lógica real

        return None  # Placeholder

    def calculate_vote_confidence(self, votes, weights):
        """Calcula confiança do voto ponderado"""
        # Confiança = 1 - entropia dos votos
        # Se todos votaram igual, confiança = 1
        # Se votos espalhados, confiança baixa

        # Simplificação
        vote_values = [v["vote"] for v in votes]
        if isinstance(vote_values[0], (int, float)):
            # Se numérico, confiança = 1 - (std / mean)
            import statistics
            std = statistics.stdev(vote_values)
            mean = statistics.mean(vote_values)
            if mean == 0:
                return 0.5
            confidence = 1 - (std / abs(mean))
            return max(0, min(1, confidence))
        else:
            # Se categórico, confiança = peso da opção mais votada
            vote_counts = defaultdict(float)
            for vote, weight in zip(vote_values, weights):
                vote_counts[vote] += weight

            return max(vote_counts.values())
```

---

## Squad Generator

```python
class SquadGenerator:
    def __init__(self):
        self.rag = RAGRetriever()

    def generate_squad(self, squad_type, project_name):
        """Gera squad do tipo especificado"""

        # Busca mente(s) para o squad
        mind_ids = self.get_minds_for_squad(squad_type, project_name)

        # Cria agents com as mentes
        agents = [Agent(mind_id) for mind_id in mind_ids]

        # Configura framework de decisão
        framework = self.get_framework_for_squad(squad_type)

        # Cria squad
        squad = Squad(
            id=f"squad_{squad_type}_{uuid4()}",
            type=squad_type,
            agents=agents,
            framework=framework
        )

        return squad

    def get_minds_for_squad(self, squad_type, project_name):
        """Busca mentes para o squad"""
        # Mapeamento de tipos de squad para tipos de mente
        MIND_MAPPING = {
            "data": ["analyst", "etl", "scraper"],
            "cognition": ["psychologist", "philosopher", "researcher"],
            "strategy": ["strategist", "consultant", "visionary"],
            "content": ["copywriter", "designer", "storyteller"],
            "automation": ["engineer", "developer", "architect"]
        }

        mind_types = MIND_MAPPING.get(squad_type, [])

        # Busca mentes no RAG
        minds = []
        for mind_type in mind_types:
            results = self.rag.retrieve(
                query=f"mente de {mind_type}",
                filters={"type": mind_type},
                top_k=1
            )

            if results:
                minds.append(results[0])

        return minds

    def get_framework_for_squad(self, squad_type):
        """Retorna framework padrão para o tipo de squad"""
        FRAMEWORK_MAPPING = {
            "data": "consensus",  # Todos devem concordar sobre os dados
            "cognition": "weighted_vote",  # Pondera por expertise
            "strategy": "expert_based",  # Estrategista decide
            "content": "weighted_vote",  # Pondera por criatividade
            "automation": "expert_based"  # Engenheiro decide
        }

        return FRAMEWORK_MAPPING.get(squad_type, "weighted_vote")
```

---

## Estrutura de Squad

```json
{
  "id": "squad_strategy_alan_nicolas_001",
  "type": "strategy",
  "agents": [
    {
      "id": "agent_strategist_001",
      "mind_id": "mind_alan_nicolas_v2",
      "role": "strategist"
    },
    {
      "id": "agent_consultant_001",
      "mind_id": "mind_alan_nicolas_v2",
      "role": "consultant"
    },
    {
      "id": "agent_visionary_001",
      "mind_id": "mind_alan_nicolas_v2",
      "role": "visionary"
    }
  ],
  "framework": "expert_based",
  "created_at": "2026-01-31T07:40:00Z",
  "stats": {
    "decisions_made": 150,
    "success_rate": 0.92
  }
}
```

---

## Integração com Orquestrador

### Task de Decisão
```python
@celery.task(name="squad.decide")
def squad_decide_task(squad_id, context):
    """Squad toma decisão (task Celery)"""
    # Carrega squad
    squad = SquadStore.get(squad_id)

    # Toma decisão
    framework = SquadDecisionFramework(squad.framework)
    decision = framework.decide(context, squad.agents)

    # Publica evento
    publish(EventType.SQUAD_DECISION_MADE, {
        "squad_id": squad_id,
        "decision": decision
    })

    return decision
```

---

## Comandos CLI

```bash
# Gerar squad
squad generate --type strategy --project alan_nicolas

# Ver squads
squad list

# Squad tomar decisão
squad decide --squad_id squad_strategy_001 --context "..."

# Ver histórico de decisões
squad history --squad_id squad_strategy_001
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Framework de decisão básico
- [ ] Squad Generator
- [ ] Histórico de decisões

### v0.5
- [ ] Aprendizado com decisões anteriores
- [ ] Expertise dinâmica
- [ ] Negociação avançada

### v1.0
- [ ] Auto-tuning de frameworks
- [ ] Squads auto-organizáveis
- [ ] Integração completa com Biblioteca de Mentes

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 7*
