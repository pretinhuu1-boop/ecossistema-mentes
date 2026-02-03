# SEGURANÇA — PRD Técnico

**Versão:** 1.0
**Data:** 2026-01-31
**Status:** Prioridade Baixa (GAP 8)

---

## Problema

**Mentes podem ter informações sensíveis**
- **Quem pode acessar QUAL mente?**

**Precisamos de:**
- Sistema de permissões
- Criptografia de mentes sensíveis
- Audit trail (quem acessou o quê quando)

---

## Stack Técnica

### Motor (Python)
- **cryptography** — Criptografia AES
- **SQLite** — Armazenamento de permissões e audit logs
- **Python** — Lógica de ACL

### Integração
- **Todos os módulos** — Checam permissões antes de acessar
- **Estado** — Registra audit trail

---

## Funcionalidades

### Core
- [ ] Sistema de permissões por mente
- [ ] Criptografia de mentes sensíveis
- [ ] Audit trail completo
- [ ] RBAC (Role-Based Access Control)

### Permissões
- [ ] Níveis de acesso (read, write, admin)
- [ ] Permissões por usuário
- [ ] Permissões por mente
- [ ] Permissões por grupo

### Criptografia
- [ ] Criptografia AES-256
- [ ] Chave de criptografia gerada automaticamente
- [ ] Descriptografia transparente (pra usuários autorizados)

### Audit Trail
- [ ] Registra todo acesso
- [ ] Quem, o quê, quando
- [ ] Logs imutáveis

---

## Controle de Acesso (RBAC)

```python
class AccessControl:
    def __init__(self):
        self.acl = ACLStore()
        self.encryption = MindEncryption()

    def check_access(self, user_id, mind_id, action="read"):
        """
        Verifica se usuário tem permissão pra ação na mente

        Args:
            user_id: ID do usuário
            mind_id: ID da mente
            action: "read", "write", "admin"

        Returns:
            bool: True se tem permissão
        """
        # 1. Verifica se mente é pública
        if self.is_public_mind(mind_id):
            return True

        # 2. Verifica permissões explícitas
        permission = self.acl.get(user_id, mind_id)
        if permission:
            return self.can_do(permission, action)

        # 3. Verifica permissões de grupo
        user_groups = self.get_user_groups(user_id)
        for group_id in user_groups:
            if self.acl.has_group_access(group_id, mind_id, action):
                return True

        # 4. Sem permissão
        return False

    def grant_access(self, admin_user_id, user_id, mind_id, permission):
        """
        Concede permissão (só admin pode)

        Args:
            admin_user_id: ID do admin concedendo permissão
            user_id: ID do usuário recebendo permissão
            mind_id: ID da mente
            permission: "read", "write", "admin"
        """
        # Verifica se admin_user é admin da mente
        if not self.check_access(admin_user_id, mind_id, "admin"):
            raise PermissionDenied("Apenas admin pode conceder permissões")

        # Concede permissão
        self.acl.grant(user_id, mind_id, permission)

        # Registra no audit trail
        self.audit_log(admin_user_id, f"granted {permission} to {user_id} on {mind_id}")

    def revoke_access(self, admin_user_id, user_id, mind_id):
        """Revoga permissão"""
        # Verifica se admin_user é admin
        if not self.check_access(admin_user_id, mind_id, "admin"):
            raise PermissionDenied("Apenas admin pode revogar permissões")

        # Revoga
        self.acl.revoke(user_id, mind_id)

        # Registra
        self.audit_log(admin_user_id, f"revoked access to {mind_id} from {user_id}")

    def can_do(self, permission, action):
        """Verifica se permissão permite ação"""
        # Hierarquia: admin > write > read
        PERMISSIONS = {
            "read": ["read"],
            "write": ["read", "write"],
            "admin": ["read", "write", "admin"]
        }

        return action in PERMISSIONS.get(permission, [])

    def is_public_mind(self, mind_id):
        """Verifica se mente é pública"""
        mind = MindStore.get(mind_id)
        return mind.get("is_public", False)

    def get_user_groups(self, user_id):
        """Retorna grupos do usuário"""
        # TODO: Implementar
        return []
```

---

## Criptografia de Mentes

```python
class MindEncryption:
    def __init__(self):
        self.cipher = Cipher(AES)

    def encrypt_mind(self, mind, is_sensitive=False):
        """
        Criptografa mente se for sensível

        Args:
            mind: Mente a criptografar
            is_sensitive: Se mente é sensível

        Returns:
            dict: Mente (criptografada se sensível)
        """
        if is_sensitive:
            # Gera chave
            key = self.generate_key()

            # Criptografa conteúdo sensível
            encrypted_content = self.cipher.encrypt(
                json.dumps(mind),
                key
            )

            # Adiciona metadata de criptografia
            mind["is_encrypted"] = True
            mind["encrypted_content"] = encrypted_content
            mind["encryption_key_hash"] = self.hash_key(key)

            # Remove conteúdo original
            del mind["artifacts"]
            del mind["signature"]

        return mind

    def decrypt_mind(self, mind, user_id):
        """
        Decriptografa mente (se usuário tiver permissão)

        Args:
            mind: Mente criptografada
            user_id: ID do usuário

        Returns:
            dict: Mente decriptografada

        Raises:
            PermissionDenied: Se usuário não tem permissão
        """
        if not mind.get("is_encrypted", False):
            return mind

        # Verifica permissão
        acl = AccessControl()
        if not acl.check_access(user_id, mind["id"], "read"):
            raise PermissionDenied("Sem permissão pra decriptografar")

        # Busca chave
        key = self.get_key(mind["encryption_key_hash"])

        # Decriptografa
        decrypted_content = self.cipher.decrypt(
            mind["encrypted_content"],
            key
        )

        # Parse de volta
        decrypted_mind = json.loads(decrypted_content)

        # Registra no audit trail
        acl.audit_log(user_id, f"decrypted {mind['id']}")

        return decrypted_mind

    def generate_key(self):
        """Gera chave de criptografia"""
        return os.urandom(32)  # 256 bits

    def hash_key(self, key):
        """Hash da chave (pra armazenar de forma segura)"""
        return hashlib.sha256(key).hexdigest()

    def get_key(self, key_hash):
        """Busca chave pelo hash (do secure store)"""
        # TODO: Implementar secure store (AWS KMS, HashiCorp Vault, etc.)
        return None  # Placeholder
```

---

## Audit Trail

```python
class AuditLogger:
    def __init__(self):
        self.db = sqlite3.connect('audit.db')
        self.init_db()

    def init_db(self):
        """Inicializa banco de audit"""
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id TEXT NOT NULL,
                action TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                resource_id TEXT NOT NULL,
                details TEXT,
                ip_address TEXT
            )
        """)
        self.db.commit()

    def log(self, user_id, action, resource_type, resource_id, details=None, ip_address=None):
        """Registra ação no audit trail"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO audit_log (timestamp, user_id, action, resource_type, resource_id, details, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            user_id,
            action,
            resource_type,
            resource_id,
            json.dumps(details) if details else None,
            ip_address
        ))
        self.db.commit()

    def query(self, user_id=None, resource_type=None, resource_id=None, from_date=None, to_date=None):
        """Consulta audit trail"""
        query = "SELECT * FROM audit_log WHERE 1=1"
        params = []

        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)

        if resource_type:
            query += " AND resource_type = ?"
            params.append(resource_type)

        if resource_id:
            query += " AND resource_id = ?"
            params.append(resource_id)

        if from_date:
            query += " AND timestamp >= ?"
            params.append(from_date)

        if to_date:
            query += " AND timestamp <= ?"
            params.append(to_date)

        cursor = self.db.cursor()
        cursor.execute(query, params)

        return cursor.fetchall()
```

---

## Integração com Módulos

### Middleware de Acesso
```python
class AccessMiddleware:
    def __init__(self):
        self.acl = AccessControl()
        self.encryption = MindEncryption()
        self.audit = AuditLogger()

    def get_mind(self, user_id, mind_id):
        """Retorna mente (com checagem de permissão)"""
        # 1. Registra tentativa de acesso
        self.audit.log(user_id, "attempt_access", "mind", mind_id)

        # 2. Verifica permissão
        if not self.acl.check_access(user_id, mind_id, "read"):
            self.audit.log(user_id, "access_denied", "mind", mind_id)
            raise PermissionDenied("Sem permissão pra acessar mente")

        # 3. Busca mente
        mind = MindStore.get(mind_id)

        # 4. Decriptografa se necessário
        if mind.get("is_encrypted", False):
            mind = self.encryption.decrypt_mind(mind, user_id)

        # 5. Registra acesso bem-sucedido
        self.audit.log(user_id, "access_granted", "mind", mind_id)

        return mind

    def update_mind(self, user_id, mind_id, updates):
        """Atualiza mente (com checagem de permissão)"""
        # Verifica permissão de write
        if not self.acl.check_access(user_id, mind_id, "write"):
            raise PermissionDenied("Sem permissão pra atualizar mente")

        # Atualiza
        MindStore.update(mind_id, updates)

        # Registra
        self.audit.log(user_id, "updated_mind", "mind", mind_id, details=updates)
```

---

## Estrutura de ACL

```json
{
  "user_id": "user_001",
  "permissions": [
    {
      "mind_id": "mind_public_001",
      "permission": "read",
      "granted_at": "2026-01-31T00:00:00Z",
      "granted_by": "system"
    },
    {
      "mind_id": "mind_sensitive_001",
      "permission": "read",
      "granted_at": "2026-01-31T00:00:00Z",
      "granted_by": "admin_001"
    },
    {
      "mind_id": "mind_001",
      "permission": "admin",
      "granted_at": "2026-01-31T00:00:00Z",
      "granted_by": "creator_001"
    }
  ]
}
```

---

## Estrutura de Audit Log

```json
{
  "id": 12345,
  "timestamp": "2026-01-31T07:40:00Z",
  "user_id": "user_001",
  "action": "access_granted",
  "resource_type": "mind",
  "resource_id": "mind_001",
  "details": {
    "permission": "read"
  },
  "ip_address": "192.168.1.100"
}
```

---

## Comandos CLI

```bash
# Conceder permissão
security grant --user user_001 --mind mind_001 --permission read

# Revogar permissão
security revoke --user user_001 --mind mind_001

# Ver permissões de usuário
security permissions --user user_001

# Ver audit trail
security audit --user user_001 --mind mind_001 --from 2026-01-01

# Criptografar mente
security encrypt --mind mind_001

# Decriptografar mente
security decrypt --mind mind_001 --user user_001
```

---

## Roadmap

### v0.1 (MVP)
- [ ] ACL básica
- [ ] Criptografia básica
- [ ] Audit trail simples

### v0.5
- [ ] RBAC completo
- [ ] Secure store de chaves
- [ ] Audit trail avançado

### v1.0
- [ ] Integração com SSO
- [ ] MFA (Multi-Factor Authentication)
- [ ] Logs imutáveis

---

*Documento v1.0 — Criado em 2026-01-31*
*Prioridade: GAP 8*
