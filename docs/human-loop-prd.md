# HUMAN-IN-THE-LOOP — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Média (GAP 4)

---

## Problema

**Hoje:**
- Loop de qualidade é 100% automático
- **Mas quem valida SE a qualidade tá realmente boa?**

**Precisamos de:**
- Pontos de "human-in-the-loop"
- Sistema de aprovação/rejeição
- Feedback loop humano → sistema aprende

---

## Stack Técnica

### Motor (Python)
- **Telegram Bot API** — Alertas e aprovações
- **SQLite** — Estado de aprovações
- **Python** — Lógica de validação

### Integração
- **Orquestrador** → Verifica se precisa de aprovação
- **Validador** → Coleta feedback humano
- **Loop de Qualidade** → Aprende com feedback

---

## Funcionalidades

### Core
- [ ] Verifica quando atingiu threshold
- [ ] Envia pedido de aprovação humana
- [ ] Coleta feedback (aprova/rejeita)
- [ ] Sistema aprende com feedback

### Pontos de Aprovação
- [ ] Threshold atingido → Pedir aprovação
- [ ] Qualidade alta mas não certeza → Pedir revisão
- [ ] Anomalias detectadas → Pedir investigação

### Feedback
- [ ] Aprovação (sim/não)
- [ ] Comentários
- [ ] Correções
- [ ] Rating de qualidade (1-5)

---

## Workflow

```
1. Loop de Qualidade avalia
   ↓
2. Atingiu threshold?
   ↓
   [NÃO] → Continua automaticamente
   ↓
   [SIM] → Pedir aprovação humana
   ↓
3. Envia alerta (Telegram)
   ↓
4. Humano aprova/rejeita
   ↓
5. Se aprovou → DONE
   ↓
6. Se rejeitou → Volta pro Loop com feedback
```

---

## Validador

```python
class HumanValidator:
    def __init__(self):
        self.telegram = TelegramClient()
        self.approval_store = ApprovalStore()

    def should_request_approval(self, metrics, threshold_level):
        """Verifica se deve pedir aprovação"""
        thresholds = THRESHOLDS[threshold_level]

        # Se atingiu threshold, pede aprovação
        if atingiu_threshold(metrics, thresholds):
            return True

        # Se qualidade tá perto mas não certeza, pede revisão
        if is_close_to_threshold(metrics, thresholds):
            return True

        # Se há anomalias, pede investigação
        if has_anomalies(metrics):
            return True

        return False

    def request_approval(self, project_name, metrics):
        """Envia pedido de aprovação"""
        # Cria pedido de aprovação
        approval_id = self.approval_store.create({
            "project_name": project_name,
            "metrics": metrics,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        })

        # Envia mensagem no Telegram
        message = f"""
🤖 *Pedido de Aprovação*

Projeto: {project_name}

Métricas:
• Cobertura: {metrics['cobertura']*100:.1f}%
• Confidence: {metrics['confidence']:.2f}
• Consistência: {metrics['consistencia']*100:.1f}%
• Gaps: {metrics['gaps']}

A qualidade atingiu o threshold. Você aprova?

/approve_{approval_id} ✅
/reject_{approval_id} ❌
/review_{approval_id} 👀
"""

        # Salva o approval_id na mensagem
        self.approval_store.update(approval_id, {
            "telegram_message_id": self.telegram.send(message)
        })

        return approval_id

    def process_approval(self, approval_id, action, feedback=""):
        """Processa feedback humano"""
        approval = self.approval_store.get(approval_id)

        if action == "approve":
            # Aprovou → DONE
            approval["status"] = "approved"
            approval["feedback"] = feedback
            approval["approved_at"] = datetime.now().isoformat()

            # Publica evento
            publish(EventType.HUMAN_APPROVED, {
                "approval_id": approval_id,
                "project_name": approval["project_name"],
                "feedback": feedback
            })

        elif action == "reject":
            # Rejeitou → Volta pro Loop
            approval["status"] = "rejected"
            approval["feedback"] = feedback
            approval["rejected_at"] = datetime.now().isoformat()

            # Publica evento
            publish(EventType.HUMAN_REJECTED, {
                "approval_id": approval_id,
                "project_name": approval["project_name"],
                "feedback": feedback
            })

        elif action == "review":
            # Precisa de revisão → Marca como "needs_review"
            approval["status"] = "needs_review"
            approval["feedback"] = feedback
            approval["reviewed_at"] = datetime.now().isoformat()

            # Publica evento
            publish(EventType.HUMAN_REVIEW, {
                "approval_id": approval_id,
                "project_name": approval["project_name"],
                "feedback": feedback
            })

        # Salva
        self.approval_store.update(approval_id, approval)

        return approval

    def learn_from_feedback(self, approval):
        """Aprende com feedback humano"""
        # TODO: Implementar aprendizado
        # Ideias:
        # - Se rejeitou, o que foi rejeitado? Ajustar thresholds?
        # - Se aprovou, o que foi aprovado? Reforçar?
        # - Se comentou, usar comentários pra melhorar extração?

        pass
```

---

## Integração com Loop de Qualidade

### Loop com Validação Humana
```python
@celery.task(name="loop.quality_with_human")
def execute_quality_loop_human(project_name, threshold_level):
    """Executa loop com validação humana"""

    # 1. Avaliar métricas
    metrics = QualityEvaluator.evaluate(project_name)

    # 2. Verificar thresholds
    thresholds = THRESHOLDS[threshold_level]

    if not atingiu_threshold(metrics, thresholds):
        # Continua automaticamente
        improver = QualityImprover(project_name)
        improver.improve(metrics, threshold_level)
        execute_quality_loop_human.delay(project_name, threshold_level)

    else:
        # 3. Verificar se precisa de aprovação
        validator = HumanValidator()

        if validator.should_request_approval(metrics, threshold_level):
            # Pedir aprovação
            approval_id = validator.request_approval(project_name, metrics)

            # Aguardar feedback
            # (isso é feito via Telegram, não bloqueia aqui)
            return {
                "status": "awaiting_approval",
                "approval_id": approval_id
            }
        else:
            # Continua automaticamente
            publish(EventType.LOOP_COMPLETED, {
                "project_name": project_name,
                "status": "done"
            })
```

### Processar Feedback
```python
@celery.task(name="human.process_feedback")
def process_human_feedback(approval_id, action, feedback=""):
    """Processa feedback humano"""
    validator = HumanValidator()
    approval = validator.process_approval(approval_id, action, feedback)

    # Aprende com feedback
    validator.learn_from_feedback(approval)

    # Se rejeitou, volta pro Loop
    if approval["status"] == "rejected":
        improver = QualityImprover(approval["project_name"])
        improver.improve_with_feedback(approval["feedback"])
        execute_quality_loop_human.delay(approval["project_name"], "enterprise")
```

---

## Integração com Clawdbot

### Telegram Bot
```python
class TelegramBot:
    def __init__(self, token):
        self.bot = Bot(token=token)

    def setup_commands(self):
        """Configura comandos do bot"""
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.bot.reply_to(message, "Bot iniciado!")

        @self.bot.message_handler(commands=['approve'])
        def handle_approve(message):
            approval_id = message.text.split('_')[1]
            process_human_feedback.delay(approval_id, "approve")

        @self.bot.message_handler(commands=['reject'])
        def handle_reject(message):
            approval_id = message.text.split('_')[1]
            feedback = " ".join(message.text.split('_')[2:])
            process_human_feedback.delay(approval_id, "reject", feedback)

        @self.bot.message_handler(commands=['review'])
        def handle_review(message):
            approval_id = message.text.split('_')[1]
            feedback = " ".join(message.text.split('_')[2:])
            process_human_feedback.delay(approval_id, "review", feedback)

    def send(self, message):
        """Envia mensagem"""
        return self.bot.send_message(CHAT_ID, message, parse_mode='Markdown')
```

---

## Estrutura de Approval

```json
{
  "id": "approval_001",
  "project_name": "alan_nicolas",
  "metrics": {
    "cobertura": 0.95,
    "confidence": 0.86,
    "consistencia": 0.92,
    "gaps": 1
  },
  "status": "pending",
  "feedback": "",
  "telegram_message_id": 12345,
  "created_at": "2026-01-31T07:40:00Z",
  "approved_at": null,
  "rejected_at": null,
  "reviewed_at": null
}
```

---

## Comandos CLI

```bash
# Ver pedidos de aprovação pendentes
human approvals pending

# Ver histórico de aprovações
human approvals history --project alan_nicolas

# Pedir aprovação manualmente
human approve --project alan_nicolas

# Ver feedback recebido
human feedback --project alan_nicolas
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Sistema de aprovação básico
- [ ] Integração com Telegram
- [ ] Loop com validação humana

### v0.5
- [ ] Feedback com comentários
- [ ] Rating de qualidade
- [ ] Histórico de aprovações

### v1.0
- [ ] Aprendizado com feedback
- [ ] Auto-tuning de thresholds
- [ ] Múltiplos aprovadores

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 4*
