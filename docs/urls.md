# Rotas (URLs)

Todas as rotas estão registradas em `core/urls.py`, que inclui os arquivos `urls.py` de cada app.

Rotas públicas não exigem autenticação. Rotas protegidas redirecionam para `/entrar/` caso o usuário não esteja logado.

---

## Públicas

| Método | URL | Nome | View | Descrição |
|---|---|---|---|---|
| GET | `/` | `landing` | `LandingPageView` | Página inicial do sistema |
| GET | `/cadastro/` | `register` | `RegisterView` | Formulário de cadastro |
| POST | `/cadastro/` | `register` | `RegisterView` | Processa o cadastro |
| GET | `/entrar/` | `login` | `LoginView` | Formulário de login |
| POST | `/entrar/` | `login` | `LoginView` | Processa o login |
| POST | `/sair/` | `logout` | `LogoutView` | Encerra a sessão e redireciona para `/` |

---

## Protegidas — Dashboard

| Método | URL | Nome | View | Descrição |
|---|---|---|---|---|
| GET | `/dashboard/` | `dashboard` | `DashboardView` | Painel principal com resumo do sistema |

---

## Protegidas — Vagas (`hub`)

| Método | URL | Nome | View | Descrição |
|---|---|---|---|---|
| GET | `/vagas/` | `job-list` | `JobListView` | Lista as vagas do usuário |
| GET | `/vagas/nova/` | `job-create` | `JobCreateView` | Formulário de nova vaga |
| POST | `/vagas/nova/` | `job-create` | `JobCreateView` | Cria a vaga |
| GET | `/vagas/<pk>/editar/` | `job-update` | `JobUpdateView` | Formulário de edição |
| POST | `/vagas/<pk>/editar/` | `job-update` | `JobUpdateView` | Salva a edição |
| POST | `/vagas/<pk>/arquivar/` | `job-archive` | `JobArchiveView` | Altera status para `archived` |

---

## Protegidas — Documentos (`documents`)

| Método | URL | Nome | View | Descrição |
|---|---|---|---|---|
| GET | `/vagas/<job_pk>/documentos/` | `document-list` | `DocumentListView` | Lista documentos de uma vaga |
| GET | `/vagas/<job_pk>/documentos/upload/` | `document-upload` | `DocumentUploadView` | Formulário de upload |
| POST | `/vagas/<job_pk>/documentos/upload/` | `document-upload` | `DocumentUploadView` | Faz o upload do PDF |
| POST | `/documentos/<pk>/status/` | `document-status` | `DocumentStatusUpdateView` | Altera o status do documento |
| POST | `/documentos/<pk>/excluir/` | `document-delete` | `DocumentDeleteView` | Exclui o documento e o arquivo |

---

## Protegidas — Análise RAG (`brain`)

| Método | URL | Nome | View | Descrição |
|---|---|---|---|---|
| GET | `/vagas/<pk>/analise/` | `job-analysis` | `JobAnalysisView` | Painel de análise de uma vaga |
| POST | `/documentos/<document_pk>/analisar/` | `document-analyze` | `DocumentAnalysisView` | Aciona o pipeline RAG para um documento |

---

## Notas

- Todas as views protegidas usam `LoginRequiredMixin`.
- Views que operam sobre objetos de outros usuários retornam 404, nunca 403, para não vazar informação de existência.
- Para gerar URLs nos templates, use sempre `{% url 'nome-da-rota' %}`.
