"""
Módulo Rastreador - MVP Foundation
"""
import time
import random
import sys
import os

# Caminho absoluto para src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from termination import Termination

class Rastreador:
    def __init__(self):
        self.termination = Termination()
        self.metrics = {
            "sources_collected": 0,
            "max_sources": 50,
            "sources_per_hour": 15,
            "min_new_sources_per_hour": 5
        }

    def run(self):
        print("🚀 Rastreador iniciado...")
        while True:
            # Simula coleta
            self.metrics["sources_collected"] += 1
            print(f"📦 Coletado: {self.metrics['sources_collected']}/{self.metrics['max_sources']}")
            
            # Check de parada
            if self.termination.should_stop("rastreador", self.metrics):
                print("🏁 Rastreador parando por critérios de exaustão/limite.")
                break
                
            time.sleep(0.1) # Simulação rápida

if __name__ == "__main__":
    r = Rastreador()
    r.run()
