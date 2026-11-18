# OrganizaTarefas — PIT Engenharia de Software II

Projeto-base independente desenvolvido para exemplificar as entregas do PIT II. **Não corresponde automaticamente à proposta elaborada pelo estudante no PIT I**.

## Requisitos
Python 3.9+; não precisa instalar bibliotecas de terceiros.

## Execução
```bash
python run.py
```
Acesse http://127.0.0.1:8000. Os registros são persistidos no arquivo local `tarefas.db` (SQLite).

## Testes automatizados
```bash
python -m unittest discover -s tests -v
```

## Funcionalidades
Cadastrar, listar, editar, concluir/reabrir, excluir e filtrar tarefas. Tratamento de campos inválidos e itens inexistentes.

## Arquitetura
- Model: `app/model.py` (repositório SQLite e validação).
- View: `app/view.py` e `static/` (HTML, CSS e JS).
- Controller: `app/controller.py` (rotas HTTP e respostas JSON).
- Inicialização: `run.py`.

## Endpoints
`GET /api/tarefas`, `GET /api/tarefas/{id}`, `POST /api/tarefas`, `PUT /api/tarefas/{id}`, `DELETE /api/tarefas/{id}`.
Corpo para POST/PUT: `{"titulo":"Estudar","descricao":"Revisar","concluida":false}`.

## Avisos
O serviço escuta somente em `127.0.0.1` e não possui autenticação. É adequado para demonstração local, **não** para exposição pública sem segurança e deploy. Links GitHub e hospedagem exigem ação do estudante. Os cinco testes por pessoas externas não foram realizados neste pacote.

## Evidência de testes (17/11/2026)

Execute `python -W error::ResourceWarning -m unittest discover -s tests -v`.
Resultado obtido: **22 testes aprovados** (7 unitários e 15 HTTP).
O histórico da execução está em `docs/resultado_testes.txt`.
Uma melhoria técnica encerra explicitamente as conexões SQLite.
**Atenção:** avaliações com cinco colegas, vídeos e publicação pública não foram realizados; esses requisitos acadêmicos dependem de participação e publicação externas.
