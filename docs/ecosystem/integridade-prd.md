# VERIFICAÇÃO DE INTEGRIDADE — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 16)

---

## Problema

**Hoje:**
- Não há verificação de integridade de dados
- Pode corromper sem notar
- Perda de dados

**Precisamos de:**
- Checksums de dados
- Verificação de integridade
- Alertas de corrupção

---

## Stack Técnica

### Motor (Python)
- **Python** — hashlib
- **SQLite** — Armazenamento de checksums

### Integração
- **Todos os módulos** — Calculam checksums antes de salvar
- **Estado** — Verifica integridade periodicamente

---

## Funcionalidades

### Core
- [ ] Cálculo de checksums
- [ ] Verificação de integridade
- [ ] Alertas de corrupção
- [ ] Reparação de dados corrompidos

---

## Verificador de Integridade

```python
class IntegrityChecker:
    def __init__(self):
        self.checksums_db = sqlite3.connect('integrity_checksums.db')
        self.init_db()

    def init_db(self):
        """Inicializa banco de checksums"""
        cursor = self.checksums_db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checksums (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                checksum TEXT NOT NULL,
                created_at TEXT NOT NULL,
                verified_at TEXT
            )
        """)
        self.checksums_db.commit()

    def calculate_checksum(self, data):
        """Calcula checksum de dados"""
        # Converte para JSON
        json_data = json.dumps(data, sort_keys=True)

        # Calcula SHA256
        checksum = hashlib.sha256(json_data.encode()).hexdigest()

        return checksum

    def save_checksum(self, data_id, data_type, data):
        """Salva checksum"""
        checksum = self.calculate_checksum(data)

        cursor = self.checksums_db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO checksums (id, type, checksum, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            data_id,
            data_type,
            checksum,
            datetime.now().isoformat()
        ))
        self.checksums_db.commit()

    def verify(self, data_id, data):
        """
        Verifica integridade de dados

        Args:
            data_id: ID dos dados
            data: Dados atuais

        Returns:
            tuple: (is_valid, current_checksum, saved_checksum)
        """
        # Calcula checksum atual
        current_checksum = self.calculate_checksum(data)

        # Busca checksum salvo
        cursor = self.checksums_db.cursor()
        cursor.execute(
            "SELECT checksum, verified_at FROM checksums WHERE id = ?",
            (data_id,)
        )
        result = cursor.fetchone()

        if not result:
            # Não tem checksum salvo, cria
            self.save_checksum(data_id, "unknown", data)
            return True, current_checksum, None

        saved_checksum, verified_at = result

        # Verifica se bate
        is_valid = current_checksum == saved_checksum

        # Atualiza verificado em
        if is_valid:
            cursor.execute(
                "UPDATE checksums SET verified_at = ? WHERE id = ?",
                (datetime.now().isoformat(), data_id)
            )
            self.checksums_db.commit()
        else:
            # CORROMPIDO!
            self.alert_corruption(data_id, current_checksum, saved_checksum)

        return is_valid, current_checksum, saved_checksum

    def alert_corruption(self, data_id, current_checksum, saved_checksum):
        """Alerta corrupção de dados"""
        print(f"🚨 CORRUPÇÃO DETECTADA!")
        print(f"Data ID: {data_id}")
        print(f"Checksum atual: {current_checksum}")
        print(f"Checksum salvo: {saved_checksum}")

        # TODO: Enviar alerta via Telegram/Email

    def verify_all(self, data_type=None):
        """
        Verifica integridade de todos os dados

        Args:
            data_type: Tipo de dados (opcional)

        Returns:
            dict: Resultado da verificação
        """
        cursor = self.checksums_db.cursor()

        query = "SELECT id, type FROM checksums"
        params = []

        if data_type:
            query += " WHERE type = ?"
            params.append(data_type)

        cursor.execute(query, params)
        all_data = cursor.fetchall()

        # Verifica cada
        results = {
            "total": len(all_data),
            "valid": 0,
            "corrupted": 0,
            "corrupted_ids": []
        }

        for data_id, dtype in all_data:
            # Busca dados atuais
            data = self.load_data(data_id, dtype)

            if data:
                # Verifica
                is_valid, _, _ = self.verify(data_id, data)

                if is_valid:
                    results["valid"] += 1
                else:
                    results["corrupted"] += 1
                    results["corrupted_ids"].append(data_id)

        return results

    def load_data(self, data_id, data_type):
        """Carrega dados (stub)"""
        # TODO: Implementar carregamento real
        return {"id": data_id, "type": data_type}

    def repair(self, data_id):
        """Repara dados corrompidos"""
        # TODO: Implementar reparação (restore de backup, etc.)
        print(f"Reparando dados {data_id}...")
        pass
```

---

## Integração

### Wrapper de Salvar com Checksum
```python
class SaveWithChecksum:
    def __init__(self, store):
        self.store = store
        self.checker = IntegrityChecker()

    def save(self, data_id, data_type, data):
        """Salva dados com checksum"""
        # Salva dados
        self.store.save(data_id, data_type, data)

        # Salva checksum
        self.checker.save_checksum(data_id, data_type, data)

        return data_id
```

### Verificação Periódica
```python
@celery.task(name="integrity.verify_all")
def verify_all_integrity():
    """Verifica integridade de todos os dados periodicamente"""
    checker = IntegrityChecker()

    # Verifica tudo
    results = checker.verify_all()

    # Se há corrupções, alerta
    if results["corrupted"] > 0:
        send_alert({
            "type": "corruption_detected",
            "corrupted_count": results["corrupted"],
            "corrupted_ids": results["corrupted_ids"],
            "urgency": "critical"
        })

    return results
```

---

## Comandos CLI

```bash
# Verificar integridade de dados específicos
integrity verify --id data_001 --type artifact

# Verificar integridade de todos os dados
integrity verify-all

# Verificar integridade por tipo
integrity verify-all --type mind

# Reparar dados corrompidos
integrity repair --id data_001

# Ver estatísticas de integridade
integrity stats
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Cálculo de checksums
- [ ] Verificação de integridade
- [ ] Alertas de corrupção

### v0.5
- [ ] Reparação automática
- [ ] Integração com backups
- [ ] Dashboard de integridade

### v1.0
- [ ] Verificação periódica automática
- [ ] Predição de corrupção
- [ ] Auto-repair avançado

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 16*
