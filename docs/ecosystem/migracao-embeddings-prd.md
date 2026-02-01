# MIGRAÇÃO DE EMBEDDINGS — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Alta (GAP 15)

---

## Problema

**Hoje:**
- Se o modelo de embedding mudar, os embeddings ficam obsoletos
- Não há estratégia de migração
- Perda de dados

**Precisamos de:**
- Migração de embeddings
- Backup automático
- Validação pós-migração

---

## Stack Técnica

### Motor (Python)
- **Python** — Lógica de migração
- **ChromaDB** — Vector store
- **SQLite** — Backup de embeddings

### Integração
- **RAG** — Detecta necessidade de migração
- **Estado** — Registra migrações

---

## Funcionalidades

### Core
- [ ] Detecção de necessidade de migração
- [ ] Backup de embeddings antigos
- [ ] Re-embeada com novo modelo
- [ ] Validação pós-migração
- [ ] Rollback se falhar

---

## Migrador de Embeddings

```python
class EmbeddingMigration:
    def __init__(self, current_model="text-embedding-3-small"):
        self.current_model = current_model
        self.chroma = ChromaDB()
        self.backup_db = sqlite3.connect('embedding_backups.db')
        self.openai = OpenAI()

    def check_migration_needed(self):
        """
        Verifica se precisa migrar embeddings

        Returns:
            tuple: (needed, old_model)
        """
        # Busca metadados dos embeddings
        metadata = self.chroma.get_metadata()

        # Se modelo atual != modelo usado, precisa migrar
        if metadata["model"] != self.current_model:
            return True, metadata["model"]

        return False, None

    def migrate(self, old_model, new_model=None):
        """
        Migra embeddings de um modelo pra outro

        Args:
            old_model: Modelo antigo
            new_model: Modelo novo (opcional, usa current_model)

        Returns:
            dict: Resultado da migração
        """
        if not new_model:
            new_model = self.current_model

        print(f"Migrando embeddings de {old_model} para {new_model}...")

        # 1. Backup dos embeddings antigos
        backup_id = self.backup_old_embeddings(old_model)
        print(f"Backup criado: {backup_id}")

        # 2. Re-embeada todos os artefatos
        artifacts = ArtifactStore.get_all()

        for i, artifact in enumerate(artifacts):
            # Gera novo embedding
            new_embedding = self.generate_embedding(artifact, new_model)

            # Atualiza no ChromaDB
            self.chroma.update(
                artifact.id,
                {
                    "vector": new_embedding,
                    "model": new_model,
                    "migrated_at": datetime.now().isoformat()
                }
            )

            if (i +1) % 100 == 0:
                print(f"Processados {i+1}/{len(artifacts)}")

        # 3. Valida qualidade
        self.validate_migration()

        print("Migração concluída com sucesso!")

        return {
            "status": "success",
            "old_model": old_model,
            "new_model": new_model,
            "backup_id": backup_id,
            "artifacts_count": len(artifacts)
        }

    def backup_old_embeddings(self, old_model):
        """Backup dos embeddings antigos"""
        backup_id = f"backup_{old_model}_{uuid4()}"

        # Busca embeddings do modelo antigo
        embeddings = self.chroma.get_all_by_model(old_model)

        # Salva no backup DB
        self.backup_db.execute("""
            CREATE TABLE IF NOT EXISTS backups (
                id TEXT PRIMARY KEY,
                model TEXT,
                artifacts_count INTEGER,
                created_at TEXT,
                embeddings TEXT
            )
        """)

        self.backup_db.execute("""
            INSERT INTO backups (id, model, artifacts_count, created_at, embeddings)
            VALUES (?, ?, ?, ?, ?)
        """, (
            backup_id,
            old_model,
            len(embeddings),
            datetime.now().isoformat(),
            json.dumps(embeddings)
        ))

        self.backup_db.commit()

        return backup_id

    def generate_embedding(self, artifact, model):
        """Gera embedding com o modelo especificado"""
        response = self.openai.embeddings.create(
            model=model,
            input=artifact["text"]
        )
        return response.data[0].embedding

    def validate_migration(self):
        """Valida qualidade da migração"""
        # Verifica se todos os embeddings foram migrados
        metadata = self.chroma.get_metadata()

        if metadata["model"] != self.current_model:
            raise MigrationError("Migração falhou: modelo não atualizado")

        # Verifica se todos os artefatos têm embeddings
        artifacts = ArtifactStore.get_all()

        for artifact in artifacts:
            embedding = self.chroma.get(artifact.id)

            if not embedding or not embedding.get("vector"):
                raise MigrationError(f"Artefato {artifact.id} sem embedding")

        print("Validação concluída com sucesso!")

    def rollback(self, backup_id):
        """Rollback para backup"""
        print(f"Rollback para backup {backup_id}...")

        # Busca backup
        cursor = self.backup_db.execute(
            "SELECT * FROM backups WHERE id = ?",
            (backup_id,)
        )
        backup = cursor.fetchone()

        if not backup:
            raise RollbackError(f"Backup {backup_id} não encontrado")

        # Restaura embeddings
        embeddings = json.loads(backup["embeddings"])

        for emb in embeddings:
            self.chroma.update(
                emb["artifact_id"],
                {
                    "vector": emb["vector"],
                    "model": backup["model"],
                    "restored_at": datetime.now().isoformat()
                }
            )

        print("Rollback concluído!")
```

---

## Integração

### Detector de Migração
```python
class MigrationDetector:
    def __init__(self):
        self.migrator = EmbeddingMigration()

    def check_and_prompt(self):
        """Verifica se precisa migrar e pergunta"""
        needed, old_model = self.migrator.check_migration_needed()

        if needed:
            print(f"⚠️ Migração necessária: {old_model} → {self.migrator.current_model}")
            print("Deseja migrar agora? (s/n)")

            response = input("> ")

            if response.lower() == 's':
                self.migrator.migrate(old_model)
            else:
                print("Migração cancelada. O sistema pode funcionar degradado.")
```

---

## Comandos CLI

```bash
# Verificar se precisa migrar
migration check

# Executar migração
migration migrate --old-model text-embedding-3-small --new-model text-embedding-3-large

# Ver histórico de migrações
migration history

# Rollback para backup
migration rollback --backup-id backup_xxx

# Validar migração atual
migration validate
```

---

## Roadmap

### v0.1 (MVP)
- [ ] Detecção de necessidade de migração
- [ ] Backup automático
- [ ] Migração básica

### v0.5
- [ ] Validação avançada
- [ ] Rollback automático
- [ ] Dashboard de migrações

### v1.0
- [ ] Migração incremental (só o que mudou)
- [ ] Migração em paralelo
- [ ] Auto-tuning de modelos

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 15*
