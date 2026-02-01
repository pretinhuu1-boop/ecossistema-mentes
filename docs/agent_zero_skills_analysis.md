# Análise de Skills do Agent Zero

Este documento apresenta uma análise detalhada das skills (ferramentas e instrumentos) disponíveis no framework [Agent Zero](https://github.com/agent0ai/agent-zero), categorizadas por funcionalidade. Estas skills servem como base para a construção das capacidades nativas do nosso ecossistema.

## 1. Comunicação e Colaboração
Ferramentas que permitem ao agente interagir com usuários e outros agentes.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **A2A Chat** | `a2a_chat.py` | Permite comunicação direta com outros agentes compatíveis com o protocolo FastA2A. Suporta envio de mensagens e anexos. |
| **Call Subordinate** | `call_subordinate.py` | Permite criar agentes subordinados (filhos) e delegar tarefas a eles. Gerencia a hierarquia e o fluxo de resposta. |
| **Notify User** | `notify_user.py` | Envia notificações para a interface do usuário com diferentes níveis de prioridade (INFO, WARNING, ALERT). |
| **Response** | `response.py` | Envia a resposta final para o usuário ou agente superior, encerrando o loop de execução atual. |

## 2. Execução de Código e Sistema
Capacidades fundamentais para operação do sistema e execução de tarefas técnicas.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Code Execution** | `code_execution_tool.py` | Ferramenta poderosa para executar código em ambientes isolados. Suporta Terminal (Bash/Shell), Python, NodeJS e conexões SSH remotas. |
| **Input** | `input.py` | Envia entrada de teclado (keystrokes) para sessões de terminal ativas. Útil para interagir com programas CLI. |
| **Wait** | `wait.py` | Pausa a execução do agente por uma duração específica ou até um horário determinado. |

## 3. Navegação Web e Pesquisa
Ferramentas para interação com a internet e extração de informações.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Browser Agent** | `browser_agent.py` | Agente de navegação autônomo baseado em `browser-use`. Capaz de realizar tarefas complexas em websites, preencher formulários e extrair dados. |
| **Search Engine** | `search_engine.py` | Realiza buscas na web utilizando SearXNG. Retorna títulos, URLs e snippets de conteúdo. |
| **YouTube Download** | `instruments/default/yt_download` | Instrumento (script) para download de vídeos do YouTube utilizando `yt-dlp`. |

## 4. Memória e Conhecimento
Gestão de memória de longo prazo e acesso a documentos.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Memory Save** | `memory_save.py` | Salva informações textuais na memória de longo prazo do agente (Vector DB), permitindo aprendizado contínuo. |
| **Memory Load** | `memory_load.py` | Recupera informações da memória utilizando busca semântica (similaridade) e filtros. |
| **Memory Forget** | `memory_forget.py` | Remove memórias que correspondem a uma busca semântica, útil para esquecer informações obsoletas. |
| **Memory Delete** | `memory_delete.py` | Remove itens específicos da memória através de seus IDs. |
| **Document Query** | `document_query.py` | Realiza perguntas sobre documentos carregados (RAG - Retrieval Augmented Generation). Suporta múltiplos documentos. |

## 5. Configuração e Gerenciamento
Controle sobre o comportamento e agendamento do agente.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Behaviour Adjustment** | `behaviour_adjustment.py` | Permite ao agente atualizar suas próprias regras de comportamento e prompt de sistema, facilitando a auto-evolução. |
| **Scheduler** | `scheduler.py` | Gerenciador completo de tarefas. Permite criar, listar e deletar tarefas agendadas (cron), ad-hoc (única execução) ou planejadas (sequência de passos). |

## 6. Visão e Mídia
Capacidades de processamento de mídia.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Vision Load** | `vision_load.py` | Carrega, comprime e processa imagens para que o agente possa "ver" e analisar seu conteúdo via modelos multimodais. |

---

## Observações para Implementação
- **Dependências**: Algumas tools dependem de bibliotecas externas (`browser-use`, `yt-dlp`, `searxng`) e serviços (Docker para execução de código segura).
- **Segurança**: A tool de execução de código (`code_execution_tool`) é extremamente poderosa e deve ser usada em ambiente sandbox.
- **Interoperabilidade**: O protocolo A2A (`a2a_chat`) é interessante para criar enxames de agentes.
