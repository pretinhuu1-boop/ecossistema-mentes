# rastreador_tasks.py
"""
Tasks do Rastreador (executados via Celery)
"""

from ..config import app
from ..publisher import publish, EventType

@app.task(name="rastreador.collect")
def collect_source(source_id: str, priority: str = "normal"):
    """
    Coleta fonte

    Args:
        source_id: ID da fonte
        priority: Prioridade da fila ("high", "normal", "low")

    Returns:
        dict: Resultado da coleta
    """
    try:
        # TODO: Implementar Rastreador
        # content = Rastreador.collect(source_id)

        # Simulação
        content = {
            "id": source_id,
            "text": f"Conteúdo da fonte {source_id}",
            "metadata": {}
        }

        # Publica evento de sucesso
        publish(EventType.SOURCE_COLLECTED, {
            "source_id": source_id,
            "content": content,
            "priority": priority
        })

        return {
            "status": "success",
            "source_id": source_id
        }

    except Exception as e:
        # Publica evento de erro
        publish(EventType.SOURCE_FAILED, {
            "source_id": source_id,
            "error": str(e)
        })

        raise
