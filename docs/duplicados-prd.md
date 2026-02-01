# DETECÇÃO DE DADOS DUPLICADOS — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Média (GAP 14)

---

## Problema

**Hoje:**
- Não detecta conteúdo duplicado
- Pode processar o mesmo conteúdo múltiplas vezes
- Ineficiente

**Precisamos de:**
- Detecção de duplicados
- Simhash/Minhash
- Otimização de processamento

---

## Stack Técnica

### Motor (Python)
- **simhash** — Detecção de similaridade
- **minhash** — Detecção de duplicados em larga escala
- **Redis** — Cache de hashes

### Integração
- **Rastreador** — Verifica antes de coletar
- **Minerador** — Verifica antes de processar

---

## Funcionalidades

### Core
- [ ] Cálculo de simhash
- [ ] Detecção de duplicados
- [ ] Cache de hashes
- [ ] Similarity threshold

---

## Detector de Duplicados

```python
class DuplicateDetector:
    def __init__(self, min_similarity=0.95):
        self.min_similarity = min_similarity
        self.redis = redis.Redis(host='localhost', port=6379, db=4)

    def is_duplicate(self, content, content_id):
        """
        Detecta se conteúdo é duplicado

        Args:
            content: Conteúdo a verificar
            content_id: ID do conteúdo

        Returns:
            tuple: (is_duplicate, duplicate_id)
        """
        # 1. Calcula simhash
        hash = self.calculate_simhash(content)

        # 2. Busca hashes similares no Redis
        similar_hashes = self.find_similar(hash)

        # 3. Se há similar > threshold, é duplicado
        if similar_hashes:
            return True, similar_hashes[0]

        # 4. Não é duplicado, salva hash
        self.save_hash(content_id, hash)

        return False, None

    def calculate_simhash(self, content):
        """Calcula simhash do conteúdo"""
        # Normaliza conteúdo
        normalized = self.normalize(content)

        # Calcula shingles (3-grams)
        shingles = self.shingles(normalized, n=3)

        # Calcula hash de cada shingle
        from hashlib import md5
        hashes = [md5(s.encode()).hexdigest() for s in shingles]

        # Converte para int
        int_hashes = [int(h, 16) for h in hashes]

        # Simhash = XOR de todos os hashes
        simhash = 0
        for h in int_hashes:
            simhash ^= h

        return simhash

    def find_similar(self, hash):
        """Busca hashes similares"""
        # Para cada hash salvo, calcula similaridade
        all_hashes = self.get_all_hashes()

        similar = []
        for existing_id, existing_hash in all_hashes:
            similarity = self.similarity(hash, existing_hash)

            if similarity >= self.min_similarity:
                similar.append(existing_id)

        return similar

    def similarity(self, hash1, hash2):
        """Calcula similaridade entre hashes"""
        # Similaridade = 1 - (hamming_distance / bits)
        bits = hash1.bit_length()
        hamming = bin(hash1 ^ hash2).count('1')

        similarity = 1 - (hamming / bits)
        return similarity

    def normalize(self, content):
        """Normaliza conteúdo (remove espaços, pontuação, etc.)"""
        # Converte para lowercase
        content = content.lower()

        # Remove pontuação
        import re
        content = re.sub(r'[^\w\s]', '', content)

        # Remove espaços extras
        content = ' '.join(content.split())

        return content

    def shingles(self, content, n=3):
        """Gera n-grams do conteúdo"""
        words = content.split()
        return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

    def save_hash(self, content_id, hash):
        """Salva hash no Redis"""
        self.redis.hset("simhashes", content_id, hash)

    def get_all_hashes(self):
        """Busca todos os hashes"""
        return self.redis.hgetall("simhashes").items()
```

---

## Integração

### Rastreador com Detecção de Duplicados
```python
class RastreadorWithDuplicateDetection:
    def __init__(self):
        self.detector = DuplicateDetector()

    def collect(self, source):
        """Coleta fonte verificando duplicados"""
        # Coleta
        content = self.raw_collect(source)

        # Verifica se é duplicado
        is_duplicate, duplicate_id = self.detector.is_duplicate(
            content["text"],
            source["id"]
        )

        if is_duplicate:
            print(f"Fonte duplicada detectada: {source['id']}")
            print(f"Duplicado de: {duplicate_id}")
            return None

        # Não é duplicado, retorna
        return content
```

---

## Comandos CLI

```bash
# Verificar duplicados
duplicates check --content "Texto aqui"

# Limpar cache de hashes
duplicates clear-cache
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Simhash básico
- [ ] Detecção de duplicados
- [ ] Cache de hashes

### v0.5
- [ ] Minhash (larga escala)
- [ ] Similarity threshold customizável
- [ ] Dashboard de duplicados

### v1.0
- [ ] Fuzzy matching
- [ ] Detecção de near-duplicates
- [ ] Auto-tuning de thresholds

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 14*
