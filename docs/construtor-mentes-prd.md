# CONSTRUTOR DE MENTES — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 5)

---

## Problema

**Hoje:**
- "Agrega artefatos em pacotes mente"
- **Mas COMO ele sabe quais artefatos pertencem a QUAL mente?**

**Precisamos de:**
- Sistema de "assinatura cognitiva" — o que define uma mente única?
- Mapeamento autor → mente (1 autor pode ter múltiplas mentes ao longo do tempo)
- Validação de mente: "Isso realmente parece a mente do Alan Nicolas?"

---

## Stack Técnica

### Motor (Python)
- **Pandas** — Análise de artefatos
- **OpenAI API** — Análise de padrões
- **ChromaDB** — Vector store

### Integração
- **Minerador** → Fornece artefatos
- **RAG** → Busca artefatos por similaridade
- **Estado** — Salva mentes construídas

---

## Funcionalidades

### Core
- [ ] Agrega artefatos por autor
- [ ] Cria assinatura cognitiva única por mente
- [ ] Valida coerência da mente
- [ ] Detecta evolução temporal (v1, v2, v3)

### Assinatura Cognitiva
- [ ] Padrões de voz (vocabulário, ritmo, estilo)
- [ ] Padrões de pensamento (como raciocina)
- [ ] Biases (o que privilegia/evita)
- [ ] Evolução (como mudou ao longo do tempo)

### Validação
- [ ] Coerência interna (artefatos consistentes entre si?)
- [ ] Coerência externa (parece a mente esperada?)
- [ ] Score de qualidade da mente (0-1)

---

## Assinatura Cognitiva

```python
class MindSignature:
    def __init__(self):
        self.openai = OpenAI()

    def analyze(self, artifacts):
        """Cria assinatura única de uma mente"""

        # 1. Análise de voz
        voice_patterns = self.analyze_voice(artifacts)

        # 2. Análise de pensamento
        thinking_patterns = self.analyze_thinking(artifacts)

        # 3. Análise de biases
        biases = self.analyze_biases(artifacts)

        # 4. Análise de evolução
        evolution = self.analyze_evolution(artifacts)

        return {
            "voice_patterns": voice_patterns,
            "thinking_patterns": thinking_patterns,
            "biases": biases,
            "evolution": evolution,
            "created_at": datetime.now().isoformat()
        }

    def analyze_voice(self, artifacts):
        """Analisa padrões de voz"""
        # Extrai texto dos artefatos
        texts = [a["content"]["description"] for a in artifacts]

        # Usa LLM pra analisar
        prompt = f"""
Analise os padrões de voz nestes textos:

{texts}

Identifique:
- Vocabulário característico (palavras frequentes)
- Ritmo e estrutura de frases
- Estilo de comunicação (formal, casual, técnico)
- Emoção predominante (entusiasmado, sério, etc.)
"""

        response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return parse_voice_analysis(response.choices[0].message.content)

    def analyze_thinking(self, artifacts):
        """Analisa padrões de pensamento"""
        # Agrupa por tipo (mental_model, heuristic, etc.)
        by_type = defaultdict(list)
        for a in artifacts:
            by_type[a["type"]].append(a)

        # Analisa cada tipo
        thinking = {}
        for type_name, type_artifacts in by_type.items():
            thinking[type_name] = self.analyze_thinking_type(type_name, type_artifacts)

        return thinking

    def analyze_biases(self, artifacts):
        """Analisa biases"""
        # Usa LLM pra identificar biases
        prompt = f"""
Analise estes artefatos cognitivos e identifique biases:

{artifacts}

Identifique:
- O que a mente privilegia
- O que a mente evita
- Temas recorrentes
- Conceitos que sempre aparecem
"""

        response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return parse_bias_analysis(response.choices[0].message.content)

    def analyze_evolution(self, artifacts):
        """Analisa evolução temporal"""
        # Ordena por data
        sorted_artifacts = sorted(artifacts, key=lambda a: a["created_at"])

        # Divide em períodos (ex: 2023, 2024, 2025, 2026)
        by_year = defaultdict(list)
        for a in sorted_artifacts:
            year = a["created_at"][:4]
            by_year[year].append(a)

        # Analisa evolução entre períodos
        evolution = []
        years = sorted(by_year.keys())

        for i in range(1, len(years)):
            prev_year = years[i-1]
            curr_year = years[i]

            prev_artifacts = by_year[prev_year]
            curr_artifacts = by_year[curr_year]

            change = self.analyze_change(prev_artifacts, curr_artifacts)

            evolution.append({
                "from": prev_year,
                "to": curr_year,
                "change": change
            })

        return evolution
```

---

## Construtor de Mentes

```python
class MindBuilder:
    def __init__(self):
        self.signature = MindSignature()
        self.rag = RAGRetriever()
        self.validator = MindValidator()

    def build(self, author_id):
        """Constrói mente completa do autor"""

        # 1. Coleta artefatos do autor
        artifacts = self.get_artifacts_by_author(author_id)

        # 2. Cria assinatura cognitiva
        signature = self.signature.analyze(artifacts)

        # 3. Valida coerência
        validation = self.validator.validate(artifacts, signature)

        # 4. Cria mente
        mind = {
            "id": f"mind_{author_id}_v{validation['version']}",
            "author_id": author_id,
            "version": validation["version"],
            "created_at": datetime.now().isoformat(),
            "artifacts": artifacts,
            "signature": signature,
            "validation": validation,
            "quality_score": validation["quality_score"]
        }

        # 5. Salva
        self.save_mind(mind)

        # 6. Publica evento
        publish(EventType.MIND_BUILT, {
            "mind_id": mind["id"],
            "author_id": author_id,
            "mind": mind
        })

        return mind

    def get_artifacts_by_author(self, author_id):
        """Coleta todos os artefatos do autor"""
        # Busca no RAG por autor
        results = self.rag.retrieve(
            query=f"Todos os artefatos de {author_id}",
            filters={"author": author_id},
            top_k=1000  # Traz tudo
        )

        return results

    def save_mind(self, mind):
        """Salva mente no banco"""
        # TODO: Implementar MindStore
        pass
```

---

## Validação de Mente

```python
class MindValidator:
    def __init__(self):
        self.openai = OpenAI()

    def validate(self, artifacts, signature):
        """Valida coerência da mente"""

        # 1. Coerência interna
        internal = self.validate_internal(artifacts)

        # 2. Coerência externa
        external = self.validate_external(artifacts, signature)

        # 3. Score geral
        quality_score = (internal["score"] + external["score"]) / 2

        return {
            "internal_coherence": internal,
            "external_coherence": external,
            "quality_score": quality_score,
            "version": self.determine_version(quality_score)
        }

    def validate_internal(self, artifacts):
        """Valida coerência interna dos artefatos"""
        # Usa LLM pra analisar
        prompt = f"""
Analise estes artefatos cognitivos e determine se são coerentes entre si:

{artifacts}

Identifique:
- Contradições
- Inconsistências
- Temas conflitantes

Retorne:
- score: 0-1 (1 = muito coerente)
- issues: lista de problemas encontrados
"""

        response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return parse_validation(response.choices[0].message.content)

    def validate_external(self, artifacts, signature):
        """Valida se parece a mente esperada"""
        # Se não tiver referência externa, usa coerência interna
        return {
            "score": 0.85,  # Simulação
            "issues": []
        }

    def determine_version(self, quality_score):
        """Determina versão da mente baseado na qualidade"""
        if quality_score > 0.9:
            return 3  # v3 (enterprise)
        elif quality_score > 0.8:
            return 2  # v2 (produção)
        else:
            return 1  # v1 (mvp)
```

---

## Estrutura de Mente

```json
{
  "id": "mind_alan_nicolas_v2",
  "author_id": "alan_nicolas",
  "version": 2,
  "created_at": "2026-01-31T07:30:00Z",
  "artifacts": [
    {
      "id": "artifact_001",
      "type": "mental_model",
      "title": "Primeiros Princípios",
      "confidence": 0.94
    }
    // ... 350 artefatos
  ],
  "signature": {
    "voice_patterns": {
      "vocabulary": ["ecossistema", "agentes", "squads", "artefatos"],
      "style": "técnico, educativo, visionário"
    },
    "thinking_patterns": {
      "mental_model": "sistêmico, modular",
      "heuristic": "iterativo, evolutivo"
    },
    "biases": {
      "privilegia": ["modularidade", "evolução"],
      "evita": ["monolitos", "estagnação"]
    },
    "evolution": [
      {
        "from": "2025",
        "to": "2026",
        "change": "Deu foco em squads e bibliotecas de mentes"
      }
    ]
  },
  "validation": {
    "internal_coherence": {
      "score": 0.92,
      "issues": []
    },
    "external_coherence": {
      "score": 0.88,
      "issues": []
    },
    "quality_score": 0.90
  }
}
```

---

## Integração com Orquestrador

### Task do Construtor
```python
@celery.task(name="construtor.build_mind")
def build_mind_task(author_id):
    """Constrói mente (task Celery)"""
    builder = MindBuilder()
    mind = builder.build(author_id)
    return mind
```

---

## Comandos CLI

```bash
# Construir mente
construtor build --author alan_nicolas

# Ver assinatura de mente
construtor signature --mind alan_nicolas_v2

# Validar mente
construtor validate --mind alan_nicolas_v2

# Comparar versões de mente
construtor compare --mind_v1 alan_nicolas_v1 --mind_v2 alan_nicolas_v2
```

---

## Roadmap

### v0.1 (MVP)
- [ ] MindSignature básico
- [ ] MindBuilder básico
- [ ] Validação de coerência interna

### v0.5
- [ ] Análise de evolução temporal
- [ ] Validação externa
- [ ] Múltiplas versões por autor

### v1.0
- [ ] Auto-aprimoramento de assinaturas
- [ ] Detecção de anomalias
- [ ] Integração completa com RAG

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 5*
