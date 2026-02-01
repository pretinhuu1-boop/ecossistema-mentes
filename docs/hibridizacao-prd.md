# HIBRIDIZAÇÃO — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Média (GAP 6)

---

## Problema

**Hoje:**
- "Combina mentes: 70% A + 30% B"
- **Mas COMO funciona essa combinação? Qual artefato de cada?**

**Precisamos de:**
- Algoritmo de hibridização
- Resolução de conflitos entre mentes
- Mistura de tom de voz

---

## Stack Técnica

### Motor (Python)
- **Pandas** — Análise e comparação de mentes
- **OpenAI API** — Resolução de conflitos
- **Python** — Lógica de combinação

### Integração
- **Construtor de Mentes** → Fornece mentes
- **RAG** → Busca artefatos similares
- **Estado** — Salva mentes híbridas

---

## Funcionalidades

### Core
- [ ] Combina mentes com pesos
- [ ] Resolve conflitos entre mentes
- [ ] Mistura artefatos complementares
- [ ] Cria assinatura cognitiva híbrida

### Resolução de Conflitos
- [ ] Artefatos conflitantes → Qual mente domina?
- [ ] Heurísticas conflitantes → Como resolver?
- [ ] Tom de voz conflitante → Como misturar?

### Validação
- [ ] Valida coerência da mente híbrida
- [ ] Detecta anomalias na combinação
- [ ] Score de qualidade da hibridização

---

## Algoritmo de Hibridização

```python
class MindHybridizer:
    def __init__(self):
        self.openai = OpenAI()
        self.resolver = ConflictResolver()
        self.validator = HybridValidator()

    def hybridize(self, minds, weights):
        """
        Combina mentes com pesos

        Args:
            minds: Lista de mentes
            weights: Lista de pesos (soma = 1.0)

        Returns:
            dict: Mente híbrida
        """
        # Valida pesos
        if sum(weights) != 1.0:
            raise ValueError("Pesos devem somar 1.0")

        # Cria mente híbrida vazia
        hybrid_mind = {
            "id": f"mind_hybrid_{uuid4()}",
            "source_minds": [
                {"mind_id": m["id"], "weight": w}
                for m, w in zip(minds, weights)
            ],
            "artifacts": [],
            "signature": {},
            "created_at": datetime.now().isoformat()
        }

        # Combina artefatos por tipo
        for artifact_type in ARTIFACT_TYPES:
            # Coleta artefatos deste tipo de todas as mentes
            type_artifacts = []
            for mind, weight in zip(minds, weights):
                type_artifacts.extend([
                    (artifact, weight)
                    for artifact in mind["artifacts"]
                    if artifact["type"] == artifact_type
                ])

            # Resolve conflitos
            resolved = self.resolver.resolve(type_artifacts, weights)

            # Adiciona à mente híbrida
            hybrid_mind["artifacts"].extend(resolved)

        # Cria assinatura híbrida
        hybrid_mind["signature"] = self.create_hybrid_signature(minds, weights)

        # Valida
        validation = self.validator.validate(hybrid_mind)
        hybrid_mind["validation"] = validation

        # Salva
        self.save_hybrid_mind(hybrid_mind)

        # Publica evento
        publish(EventType.HYBRID_MIND_CREATED, {
            "hybrid_mind_id": hybrid_mind["id"],
            "source_minds": [m["id"] for m in minds],
            "weights": weights
        })

        return hybrid_mind

    def create_hybrid_signature(self, minds, weights):
        """Cria assinatura cognitiva híbrida"""
        # Combina assinaturas com pesos
        hybrid_signature = {
            "voice_patterns": self.combine_voices(minds, weights),
            "thinking_patterns": self.combine_thinking(minds, weights),
            "biases": self.combine_biases(minds, weights),
            "evolution": None  # Mente híbrida não tem evolução própria
        }

        return hybrid_signature

    def combine_voices(self, minds, weights):
        """Combina padrões de voz"""
        # Para cada aspecto da voz, combina com pesos
        hybrid_voice = {}

        for aspect in ["vocabulary", "style", "emotion"]:
            # Coleta valores de todas as mentes
            values = [
                (mind["signature"]["voice_patterns"][aspect], weight)
                for mind, weight in zip(minds, weights)
            ]

            # Pondera (se aspect for string, usa weighted voting)
            if isinstance(values[0][0], str):
                # Weighted voting
                votes = defaultdict(float)
                for value, weight in values:
                    votes[value] += weight

                # Pega o mais votado
                hybrid_voice[aspect] = max(votes.items(), key=lambda x: x[1])[0]

            else:
                # Weighted average (se for numérico)
                hybrid_voice[aspect] = sum(v * w for v, w in values) / sum(weights)

        return hybrid_voice

    def combine_thinking(self, minds, weights):
        """Combina padrões de pensamento"""
        # Similar a voz, mas para thinking_patterns
        hybrid_thinking = {}

        for type_name in ARTIFACT_TYPES:
            # Coleta valores
            values = [
                (mind["signature"]["thinking_patterns"].get(type_name, {}), weight)
                for mind, weight in zip(minds, weights)
            ]

            # Combina (merge com pesos)
            hybrid_thinking[type_name] = {}
            all_keys = set()
            for value, _ in values:
                all_keys.update(value.keys())

            for key in all_keys:
                # Weighted average
                hybrid_thinking[type_name][key] = sum(
                    value.get(key, 0) * weight
                    for value, weight in values
                ) / sum(weights)

        return hybrid_thinking

    def combine_biases(self, minds, weights):
        """Combina biases"""
        hybrid_biases = {
            "privilegia": [],
            "evita": []
        }

        # Coleta todos os "privilegia" com pesos
        for mind, weight in zip(minds, weights):
            for bias in mind["signature"]["biases"]["privilegia"]:
                hybrid_biases["privilegia"].append({
                    "bias": bias,
                    "weight": weight,
                    "source_mind": mind["id"]
                })

        # Coleta todos os "evita" com pesos
        for mind, weight in zip(minds, weights):
            for bias in mind["signature"]["biases"]["evita"]:
                hybrid_biases["evita"].append({
                    "bias": bias,
                    "weight": weight,
                    "source_mind": mind["id"]
                })

        return hybrid_biases
```

---

## Resolvedor de Conflitos

```python
class ConflictResolver:
    def __init__(self):
        self.openai = OpenAI()

    def resolve(self, type_artifacts, weights):
        """
        Resolve conflitos entre artefatos

        Args:
            type_artifacts: Lista de (artifact, weight)
            weights: Lista de pesos (uma por mente)

        Returns:
            list: Lista de artefatos resolvidos
        """
        # Detecta conflitos
        conflicts = self.detect_conflicts(type_artifacts)

        # Resolve cada conflito
        resolved = []
        for conflict in conflicts:
            resolution = self.resolve_conflict(conflict, weights)
            resolved.append(resolution)

        # Adiciona artefatos não conflitantes
        non_conflicting = [
            artifact for artifact, _ in type_artifacts
            if not any(c["artifact"] == artifact for c in conflicts)
        ]
        resolved.extend(non_conflicting)

        return resolved

    def detect_conflicts(self, type_artifacts):
        """Detecta conflitos entre artefatos"""
        # Agrupa por similaridade
        groups = self.group_by_similarity(type_artifacts)

        # Para cada grupo, verifica se há conflito
        conflicts = []
        for group in groups:
            if len(group) > 1:
                # Conflito detectado
                conflicts.append({
                    "type": "conflict",
                    "artifacts": group
                })

        return conflicts

    def group_by_similarity(self, type_artifacts):
        """Agrupa artefatos por similaridade"""
        # Calcula similaridade entre todos os pares
        # Se similaridade > threshold, agrupa

        # Simplificação: agrupa por título
        by_title = defaultdict(list)
        for artifact, weight in type_artifacts:
            by_title[artifact["title"]].append((artifact, weight))

        return list(by_title.values())

    def resolve_conflict(self, conflict, weights):
        """
        Resolve conflito

        Estratégias:
        1. Dominância de peso → mente com maior peso domina
        2. Consenso → todos concordam?
        3. Experto → especialista naquele tema decide
        4. Fusão → funde artefatos
        """
        artifacts = conflict["artifacts"]

        # Estratégia 1: Dominância de peso
        max_weight = max(weights)
        max_mind_index = weights.index(max_weight)

        if max_weight > 0.6:
            # Mente dominante decide
            return artifacts[max_mind_index][0]

        # Estratégia 2: Consenso
        if all(a[0]["content"] == artifacts[0][0]["content"] for a in artifacts):
            # Todos concordam, retorna qualquer um
            return artifacts[0][0]

        # Estratégia 3: Experto
        # TODO: Implementar detecção de especialista

        # Estratégia 4: Fusão
        return self.fuse_artifacts(artifacts, weights)

    def fuse_artifacts(self, artifacts, weights):
        """Funde artefatos conflitantes"""
        # Usa LLM pra fundir
        prompt = f"""
Fundir estes artefatos cognitivos em um único:

{artifacts}

Crie um novo artefato que combine o melhor de cada um,
considerando os pesos: {weights}
"""

        response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse response
        fused = parse_fused_artifact(response.choices[0].message.content)

        # Adiciona metadata de fusão
        fused["metadata"]["fused_from"] = [a[0]["id"] for a in artifacts]
        fused["metadata"]["fusion_weights"] = weights

        return fused
```

---

## Validação de Híbrido

```python
class HybridValidator:
    def __init__(self):
        self.openai = OpenAI()

    def validate(self, hybrid_mind):
        """Valida coerência da mente híbrida"""

        # 1. Coerência interna
        internal = self.validate_internal_coherence(hybrid_mind)

        # 2. Coerência com mentes fonte
        source_coherence = self.validate_source_coherence(hybrid_mind)

        # 3. Anomalias
        anomalies = self.detect_anomalies(hybrid_mind)

        # Score geral
        quality_score = (internal["score"] + source_coherence["score"]) / 2

        # Se há anomalias, reduz score
        if anomalies:
            quality_score = quality_score * 0.9

        return {
            "internal_coherence": internal,
            "source_coherence": source_coherence,
            "anomalies": anomalies,
            "quality_score": quality_score
        }

    def validate_internal_coherence(self, hybrid_mind):
        """Valida coerência interna"""
        # Mesma lógica que MindValidator
        return {
            "score": 0.88,  # Simulação
            "issues": []
        }

    def validate_source_coherence(self, hybrid_mind):
        """Valida se híbrido parece com as mentes fonte"""
        # Usa LLM pra analisar
        prompt = f"""
Analise esta mente híbrida e as mentes fonte:

HÍBRIDO:
{hybrid_mind["signature"]}

FONTES:
{[m["signature"] for m in hybrid_mind["source_minds"]]}

A mente híbrida parece coerente com as fontes?
É uma combinação lógica?
"""

        response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return parse_coherence_analysis(response.choices[0].message.content)

    def detect_anomalies(self, hybrid_mind):
        """Detecta anomalias na combinação"""
        anomalies = []

        # Anomalia 1: Artefatos duplicados
        artifact_ids = [a["id"] for a in hybrid_mind["artifacts"]]
        if len(artifact_ids) != len(set(artifact_ids)):
            anomalies.append({
                "type": "duplicate_artifacts",
                "message": "Mente híbrida tem artefatos duplicados"
            })

        # Anomalia 2: Padrões de voz muito diferentes
        voice = hybrid_mind["signature"]["voice_patterns"]
        if self.voice_too_different(voice):
            anomalies.append({
                "type": "voice_conflict",
                "message": "Padrões de voz muito diferentes"
            })

        return anomalies

    def voice_too_different(self, voice):
        """Verifica se voz é muito diferente"""
        # Simplificação: se tiver muitos valores únicos, é muito diferente
        # TODO: Implementar melhor
        return False
```

---

## Estrutura de Mente Híbrida

```json
{
  "id": "mind_hybrid_gary_vaynerchuk_seth_godin_001",
  "source_minds": [
    {"mind_id": "mind_gary_vaynerchuk_v2", "weight": 0.7},
    {"mind_id": "mind_seth_godin_v1", "weight": 0.3}
  ],
  "artifacts": [
    {
      "id": "artifact_hybrid_001",
      "type": "mental_model",
      "title": "Conteúdo em Escala",
      "content": "...",
      "metadata": {
        "fused_from": ["artifact_gv_001", "artifact_sg_001"],
        "fusion_weights": [0.7, 0.3]
      }
    }
  ],
  "signature": {
    "voice_patterns": {
      "vocabulary": ["hustle", "marketing", "storytelling"],
      "style": "energético + reflexivo"
    },
    "thinking_patterns": {
      "mental_model": "escala + permissão",
      "heuristic": "rápido + lento"
    },
    "biases": {
      "privilegia": [
        {"bias": "ação", "weight": 0.7, "source_mind": "mind_gary_vaynerchuk_v2"},
        {"bias": "permissoes", "weight": 0.3, "source_mind": "mind_seth_godin_v1"}
      ],
      "evita": [
        {"bias": "perfeccionismo", "weight": 0.5, "source_mind": "mind_gary_vaynerchuk_v2"}
      ]
    },
    "evolution": null
  },
  "validation": {
    "internal_coherence": {
      "score": 0.88,
      "issues": []
    },
    "source_coherence": {
      "score": 0.92,
      "issues": []
    },
    "anomalies": [],
    "quality_score": 0.90
  },
  "created_at": "2026-01-31T07:40:00Z"
}
```

---

## Integração com Orquestrador

### Task de Hibridização
```python
@celery.task(name="hibridizador.hybridize")
def hybridize_task(mind_ids, weights):
    """Hibridiza mentes (task Celery)"""
    # Carrega mentes
    minds = [MindStore.get(mid) for mid in mind_ids]

    # Hibridiza
    hybridizer = MindHybridizer()
    hybrid_mind = hybridizer.hybridize(minds, weights)

    return hybrid_mind
```

---

## Comandos CLI

```bash
# Hibridizar mentes
hibridizador hybridize --minds mind_001,mind_002 --weights 0.7,0.3

# Ver mentes híbridas
hibridizador list

# Comparar mente híbrida com fontes
hibridizador compare --hybrid mind_hybrid_001

# Ver conflitos resolvidos
hibridizador conflicts --hybrid mind_hybrid_001
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Algoritmo de hibridização básico
- [ ] Resolução de conflitos por peso
- [ ] Validação de híbrido

### v0.5
- [ ] Fusão de artefatos
- [ ] Detecção de especialista
- [ ] Análise de anomalias

### v1.0
- [ ] Hibridização recursiva (mentes de mentes)
- [ ] Auto-tuning de pesos
- [ ] Histórico de hibridizações

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 6*
