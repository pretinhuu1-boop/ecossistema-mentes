import logging
import os
from datetime import datetime

class AlertManager:
    """Gerenciador de Alertas simples para Health Check"""
    
    def __init__(self, log_path: str = "./logs/health_alerts.log"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        logging.basicConfig(
            filename=self.log_path,
            level=logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("HealthAlerts")

    def notify(self, module: str, status: str, message: str):
        """Registra alerta no log e futuramente envia notificações (Telegram/Slack)"""
        alert_msg = f"Module: {module} | Status: {status} | Message: {message}"
        self.logger.warning(alert_msg)
        print(f"⚠️ ALERT: {alert_msg}")

    def process_results(self, results: dict):
        """Processa resultados da engine e notifica se necessário"""
        for module, data in results.get('modules', {}).items():
            if data.get('status') in ['unhealthy', 'error']:
                self.notify(module, data['status'], data.get('error', 'Unknown error'))
            elif data.get('status') == 'degraded':
                self.notify(module, 'degraded', data.get('warning', 'Degraded performance'))
