# Documentação técnica
## Escopo
Sistema web local para controle individual de tarefas. MVP: criar, listar, alterar, marcar concluída, reabrir, excluir e filtrar. Fora de escopo: usuários, login, notificações, colaboração e hospedagem pública.

## Requisitos funcionais
RF01 cadastrar tarefa com título; RF02 listar tarefas; RF03 editar título e descrição; RF04 marcar como concluída/reaberta; RF05 excluir após confirmação; RF06 filtrar por estado.

## Requisitos não funcionais
RNF01 interface responsiva; RNF02 feedback das ações; RNF03 armazenamento SQLite; RNF04 validação no servidor; RNF05 não exigir dependências externas para execução local.

## Casos de uso (resumo)
Ator: usuário local. UC01 gerenciar tarefas (inclusões, alterações, exclusões); UC02 acompanhar tarefas (listagem, filtro, conclusão). Fluxo alternativo: entradas inválidas geram HTTP 400 e mensagem; ID não localizado gera HTTP 404.

## Diagrama de classe (texto)
`TaskRepository` contém `initialize`, `list_all`, `get`, `add`, `update` e `delete`. Entidade `Tarefa`: id:int, titulo:str, descricao:str, concluida:bool, criada_em:datetime. O controlador invoca o repositório e emite resposta HTTP; a interface consome endpoints com fetch.

## DER / esquema lógico
TAREFAS(id PK, titulo NOT NULL, descricao NOT NULL, concluida NOT NULL, criada_em NOT NULL). Não há tabelas relacionadas na versão inicial; modelo normalizado sem grupos repetitivos.

## Dicionário de dados
| Campo | Tipo SQLite | Regra |
|---|---|---|
| id | INTEGER | PK autoincremento |
| titulo | TEXT | obrigatório, 1–100 caracteres após trim |
| descricao | TEXT | até 500 caracteres; padrão vazio |
| concluida | INTEGER | 0 ou 1; padrão 0 |
| criada_em | TEXT | instante UTC ISO 8601 |

## IHC/UX
Formulário com rótulos, limite de caracteres, feedback em região `aria-live`, caixa de confirmação de exclusão, botões claramente identificados, filtro com três estados, responsividade por CSS.

## Testes
Testes unitários do repositório em `tests/test_model.py`. Validação externa com cinco pessoas precisa ser realizada, documentada e anexada pelo estudante; não houve simulação de participantes.
