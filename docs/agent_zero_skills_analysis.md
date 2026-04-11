# Análise de Skills do Agent Zero

Este documento apresenta uma análise detalhada das skills (ferramentas e instrumentos), agentes (mentes) e estrutura de conhecimento disponíveis no framework [Agent Zero](https://github.com/agent0ai/agent-zero). Estas capacidades servem como base para a construção das capacidades nativas do nosso ecossistema.

## 1. Mentes Base (Agentes)
O framework fornece "personas" ou "mentes" especializadas que atuam como o cérebro do sistema. Estas são as mentes que servirão como "database" inicial de inteligência para criar novos ecossistemas.

| Agente | Perfil | Capacidades Principais |
|--------|--------|------------------------|
| **Agent 0** | Generalista | Agente raiz. Gerencia outros agentes, delega tarefas e possui acesso a todas as ferramentas. Atua como orquestrador. |
| **Developer** | Engenheiro de Software | Especializado em escrever, depurar e executar código (Python, NodeJS, Shell). Focado em construção de software e automação. |
| **Researcher** | Pesquisador (Deep ReSearch) | Especializado em busca profunda, validação de fontes, análise de dados e síntese de relatórios complexos. Executa protocolos rigorosos de pesquisa acadêmica e de mercado. |
| **Hacker** | Especialista em Segurança | Focado em testes de penetração, análise de vulnerabilidades e segurança ofensiva/defensiva (em ambientes controlados). |

Estas mentes são definidas por seus **System Prompts** (localizados em `agents/*/prompts/`), que contêm as instruções cognitivas, metodologias e restrições de cada perfil.

## 2. Estrutura de Conhecimento (Database)
O sistema utiliza uma estrutura de pastas para armazenar conhecimento estático e dinâmico, que alimenta o RAG (Retrieval Augmented Generation).

- **Knowledge Base (`knowledge/`)**:
    - `default/`: Conhecimento padrão que vem com o sistema (ex: documentação do próprio Agent Zero em `knowledge/default/main/about`).
    - `custom/`: Espaço reservado para o conhecimento específico do nosso projeto (ECOSSISTEMA DE MENTES). É aqui que os "artefatos cognitivos" minerados devem ser armazenados.
    - Estrutura interna: Dividido em `main` (conhecimento geral) e `solutions` (memória de soluções passadas).

## 3. Comunicação e Colaboração (Tools)
Ferramentas que permitem ao agente interagir com usuários e outros agentes.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **A2A Chat** | `a2a_chat.py` | Permite comunicação direta com outros agentes compatíveis com o protocolo FastA2A. Suporta envio de mensagens e anexos. |
| **Call Subordinate** | `call_subordinate.py` | Permite criar agentes subordinados (filhos) e delegar tarefas a eles. Gerencia a hierarquia e o fluxo de resposta. |
| **Notify User** | `notify_user.py` | Envia notificações para a interface do usuário com diferentes níveis de prioridade (INFO, WARNING, ALERT). |
| **Response** | `response.py` | Envia a resposta final para o usuário ou agente superior, encerrando o loop de execução atual. |

## 4. Execução de Código e Sistema (Tools)
Capacidades fundamentais para operação do sistema e execução de tarefas técnicas.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Code Execution** | `code_execution_tool.py` | Ferramenta poderosa para executar código em ambientes isolados. Suporta Terminal (Bash/Shell), Python, NodeJS e conexões SSH remotas. |
| **Input** | `input.py` | Envia entrada de teclado (keystrokes) para sessões de terminal ativas. Útil para interagir com programas CLI. |
| **Wait** | `wait.py` | Pausa a execução do agente por uma duração específica ou até um horário determinado. |

## 5. Navegação Web e Pesquisa (Tools)
Ferramentas para interação com a internet e extração de informações.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Browser Agent** | `browser_agent.py` | Agente de navegação autônomo baseado em `browser-use`. Capaz de realizar tarefas complexas em websites, preencher formulários e extrair dados. |
| **Search Engine** | `search_engine.py` | Realiza buscas na web utilizando SearXNG. Retorna títulos, URLs e snippets de conteúdo. |
| **YouTube Download** | `instruments/default/yt_download` | Instrumento (script) para download de vídeos do YouTube utilizando `yt-dlp`. |

## 6. Memória e Conhecimento (Tools)
Gestão de memória de longo prazo e acesso a documentos.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Memory Save** | `memory_save.py` | Salva informações textuais na memória de longo prazo do agente (Vector DB), permitindo aprendizado contínuo. |
| **Memory Load** | `memory_load.py` | Recupera informações da memória utilizando busca semântica (similaridade) e filtros. |
| **Memory Forget** | `memory_forget.py` | Remove memórias que correspondem a uma busca semântica, útil para esquecer informações obsoletas. |
| **Memory Delete** | `memory_delete.py` | Remove itens específicos da memória através de seus IDs. |
| **Document Query** | `document_query.py` | Realiza perguntas sobre documentos carregados (RAG - Retrieval Augmented Generation). Suporta múltiplos documentos. |

## 7. Configuração e Gerenciamento (Tools)
Controle sobre o comportamento e agendamento do agente.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Behaviour Adjustment** | `behaviour_adjustment.py` | Permite ao agente atualizar suas próprias regras de comportamento e prompt de sistema, facilitando a auto-evolução. |
| **Scheduler** | `scheduler.py` | Gerenciador completo de tarefas. Permite criar, listar e deletar tarefas agendadas (cron), ad-hoc (única execução) ou planejadas (sequência de passos). |

## 8. Visão e Mídia (Tools)
Capacidades de processamento de mídia.

| Skill | Arquivo | Descrição |
|-------|---------|-----------|
| **Vision Load** | `vision_load.py` | Carrega, comprime e processa imagens para que o agente possa "ver" e analisar seu conteúdo via modelos multimodais. |

---

## Observações para o Ecossistema
- **Mentes como Database**: Os arquivos em `agents/` (especialmente os prompts) são o "código-fonte" das mentes. Para criar novos ecossistemas, suas mentes usarão estes templates como base, modificando os prompts para especializar o novo agente.
- **Tools como Habilidades**: As ferramentas listadas (Code, Browser, etc.) são as habilidades que podem ser plugadas nessas novas mentes.
