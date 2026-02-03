---
name: ecossistema-mentes
description: Acesso ao Ecossistema de Mentes (Rastrear, Minerar, Construir, Squads).
metadata: { "openclaw": { "emoji": "🧠", "requires": { "bins": ["python3"] } } }
---

# Ecossistema de Mentes

Use este skill para interagir com o Ecossistema de Mentes. Você pode rastrear fontes, minerar artefatos cognitivos, construir mentes e executar tarefas com squads.

## Comandos

O CLI principal está localizado em `ecosystem/src/cli.py`.

### 1. Rastrear Fontes
Coleta dados de fontes externas (URLs, vídeos, etc.).

```bash
python3 ecosystem/src/cli.py rastrear --target "URL_OU_TEMA"
```

### 2. Minerar Artefatos
Processa os dados coletados para extrair modelos mentais e heurísticas.

```bash
python3 ecosystem/src/cli.py minerar --source "latest"
```

### 3. Construir Mente
Cria ou atualiza uma Mente baseada em um autor/persona.

```bash
python3 ecosystem/src/cli.py construir_mente --author "Nome do Autor"
```

### 4. Executar Squad
Delega uma tarefa para um Squad gerido por uma Mente específica.

```bash
python3 ecosystem/src/cli.py squad_task --mind_id "mind_alan_nicolas_v1" --skill "copywriting" --task "Escrever email de vendas"
```

## Fluxo de Trabalho Típico

1.  **Rastrear**: `python3 ecosystem/src/cli.py rastrear --target "Alan Nicolas YouTube"`
2.  **Minerar**: `python3 ecosystem/src/cli.py minerar`
3.  **Construir**: `python3 ecosystem/src/cli.py construir_mente --author "Alan Nicolas"`
4.  **Executar**: `python3 ecosystem/src/cli.py squad_task ...`

Sempre verifique a saída JSON para confirmar o sucesso (`"status": "completed"`).
