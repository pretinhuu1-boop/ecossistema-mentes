# VALIDAÇÃO DE QUALIDADE DE DADOS — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 13)

---

## Problema

**Hoje:**
- Nenhum módulo valida qualidade dos dados
- Pode processar lixo
- Não distingue spam de conteúdo real

**Precisamos de:**
- Validação de qualidade de dados
- Filtros de spam
- Pontuação de qualidade (score 0-1)

---

## Stack Técnica

### Motor (Python)
- **Python** — Lógica de validação
- **textstat** — Métricas de legibilidade
- **langdetect** — Detecção de língua

### Integração
- **Rastreador** — Valida antes de processar
- **Minerador** — Valida antes de extrair
- **Estado** — Registra scores de qualidade

---

## Funcionalidades

### Core
- [ ] Validação de conteúdo
- [ ] Validação de vídeo/áudio
- [ ] Detecção de spam
- [ ] Score de qualidade (0-1)

### Critérios de Qualidade

#### Conteúdo (Texto)
- `min_length` — Mínimo de caracteres
- `max_repetition` — Máximo de repetição
- `readability_score` — Mínimo de legibilidade
- `language_detection` — Deve detectar língua

#### Vídeo
- `min_duration` — Mínimo de segundos
- `max_duration` — Máximo de segundos
- `min_resolution` — Mínimo de resolução
- `audio_track` — Deve ter áudio

#### Áudio
- `min_duration` — Mínimo de segundos
- `max_duration` — Máximo de segundos
- `min_bitrate` — Mínimo de kbps
- `language_detection` — Deve detectar língua

---

## Validador de Qualidade

```python
class DataQualityValidator:
    def __init__(self):
        self.readability = ReadabilityCalculator()
        self.language = LanguageDetector()
        self.spam_detector = SpamDetector()

    def validate(self, data, source_type):
        """
        Valida qualidade dos dados

        Args:
            data: Dados a validar
            source_type: Tipo de fonte ("content", "video", "audio")

        Returns:
            dict: Resultado da validação
        """
        # Seleciona validador por tipo
        validators = {
            "content": self.validate_content,
            "video": self.validate_video,
            "audio": self.validate_audio
        }

        validator = validators.get(source_type, lambda x: self.validate_unknown(x))
        result = validator(data)

        # Adiciona score geral
        result["overall_score"] = self.calculate_overall_score(result)
        result["passed"] = result["overall_score"] >= 0.7

        return result

    def validate_content(self, data):
        """Valida conteúdo de texto"""
        text = data.get("text", "")

        # Critérios
        criteria = {
            "min_length": len(text) >= 100,
            "max_repetition": self.check_repetition(text) <= 0.3,
            "readability_score": self.readability.calculate(text) >= 0.5,
            "language_detection": self.language.detect(text) is not None,
            "not_spam": not self.spam_detector.is_spam(text)
        }

        # Calcula score
        score = sum(criteria.values()) / len(criteria)

        return {
            "type": "content",
            "score": score,
            "criteria": criteria,
            "language": self.language.detect(text),
            "readability": self.readability.calculate(text)
        }

    def check_repetition(self, text):
        """Verifica repetição de texto"""
        words = text.split()
        if len(words) < 10:
            return 0.0

        unique_words = len(set(words))
        repetition = 1 - (unique_words / len(words))

        return repetition
```

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 13*
