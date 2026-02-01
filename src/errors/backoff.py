import random
import time

class ExponentialBackoff:
    """Implementa cálculo de tempo de espera exponencial com jitter."""
    
    def __init__(self, base: float = 1.0, max_wait: float = 60.0):
        self.base = base
        self.max_wait = max_wait

    def calculate(self, retry_count: int) -> float:
        """
        Calcula o próximo tempo de espera.
        Fórmula: min(base * (2^retry_count), max_wait) + jitter
        """
        wait_time = min(self.base * (2 ** retry_count), self.max_wait)
        
        # Adiciona jitter aleatório (0-10% do wait_time)
        jitter = wait_time * 0.1 * random.random()
        return wait_time + jitter

    def wait(self, retry_count: int):
        """Calcula e aguarda o tempo necessário."""
        wait_time = self.calculate(retry_count)
        time.sleep(wait_time)
        return wait_time
