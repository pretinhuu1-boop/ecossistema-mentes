"""
Módulo Minerador - MVP Foundation
"""
import sys
import os

# Caminho absoluto para src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from termination import Termination

class Minerador:
    def __init__(self):
        self.termination = Termination()
        # No Minerador, a parada geralmente ocorre após processar um lote
        self.batch_metrics = {
            "artifacts_per_source": 120, # Acima do limite de 100 definido nos exemplos
            "confidence_mean": 0.85
        }

    def process_batch(self):
        print("⛏️ Minerando lote de fontes...")
        
        # Check de parada
        if self.termination.should_stop("minerador", self.batch_metrics):
            print("🏁 Minerador parando: densidade de artefatos por fonte muito alta (Threshold atingido).")
            return False
        return True

if __name__ == "__main__":
    m = Minerador()
    m.process_batch()
