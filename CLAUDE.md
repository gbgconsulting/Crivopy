# CLAUDE.md — Crivopy

Guia de referência rápida para o Claude trabalhar neste projeto. Leia antes de qualquer implementação.

---

## O que é o projeto

**Crivopy** é um sistema web de triagem de currículos e documentos PDF. Usuários autenticados criam vagas, fazem upload de currículos em PDF e utilizam análise via IA (RAG) para pontuar a aderência de cada candidato ao perfil da vaga.

Documentação completa em `docs/`. PRD completo em `docs/../PRD.md`.

---

## Stack

- **Python 3.13** + **Django 5.x** — full stack, sem API REST separada
- **SQLite** — banco de dados padrão do Django, sem configuração adicional
- **Django Template Language** + **TailwindCSS via CDN** — frontend server-side
- **PyMuPDF**, **Sentence Transformers**, **ChromaDB**, **OpenAI** — pipeline RAG

---

## Estrutura de apps

```
core/       → settings, urls raiz, wsgi/asgi — sem models nem views de negócio
users/      → User customizado, login por e-mail, cadastro, logout
hub/        → Job (vaga) — criação, listagem, edição, arquivamento
documents/  → Document (currículo PDF) — upload, listagem, status, exclusão
brain/      → Analysis, DocumentChunk, pipeline RAG (brain/services/)
chat/       → placeholder, sem funcionalidade ativa
```

Templates ficam em `templates/` na raiz. Arquivos enviados em `media/`. Índice vetorial em `chroma_db/`.

---

## Regras de código — seguir sempre

**Linguagem:** código em inglês, interface ao usuário em português brasileiro.

**Estilo:** PEP 8, aspas simples em todo o código Python.

**Views:** usar Class-Based Views. `LoginRequiredMixin` sempre como primeiro na herança. Sobrescrever `get_queryset` filtrando por `request.user` — nunca confiar só no `pk` da URL.

**Models:** todo model herda de `models.Model`, tem `created_at = models.DateTimeField(auto_now_add=True)` e `updated_at = models.DateTimeField(auto_now=True)`, tem `__str__` definido. Choices como constantes de classe.

**Forms:** `ModelForm` para forms que mapeiam para models. Classes CSS do design system aplicadas nos widgets via `attrs`.

**Signals:** ficam em `<app>/signals.py`. Conectados no `ready()` do `<app>/apps.py`.

**URLs:** nomes em kebab-case (`job-list`, `document-upload`). Usar `reverse_lazy()` nas views, `{% url %}` nos templates. Nunca URLs hardcoded.

**Templates:** herdam de `base.html` ou `base_authenticated.html`. Variáveis de contexto em snake_case. Mensagens via `{% include 'partials/_messages.html' %}`. `{% csrf_token %}` obrigatório em todo `<form>` POST.

**Segurança:** validar extensão `.pdf` e tipo MIME `application/pdf` no `clean()` do form de upload. Views de update/delete filtram por `request.user`, retornam 404 para objetos de outros usuários.

**Sem over-engineering:** preferir recursos nativos do Django. Não adicionar dependências sem necessidade clara.

---

## Design system — resumo

Dark mode exclusivo. Fundo `bg-gray-950`, cards `bg-gray-900`, inputs `bg-gray-800`. Gradiente primário `from-indigo-600 to-violet-600`. Fonte Inter via Google Fonts.

Detalhes completos em `docs/design-system.md`.

```html
<!-- Botão primário -->
<button class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-semibold text-sm hover:from-indigo-500 hover:to-violet-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-950 transition-all duration-200 shadow-lg shadow-indigo-900/40">

<!-- Input -->
<input class="w-full px-4 py-2.5 rounded-xl bg-gray-800 border border-gray-700 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200">

<!-- Card -->
<div class="bg-gray-900 border border-gray-800 rounded-2xl p-6 hover:border-gray-700 transition-all duration-200 shadow-xl shadow-black/20">
```

Badges de status: `bg-blue-500/10 text-blue-400` (pendente), `bg-amber-500/10 text-amber-400` (em análise), `bg-emerald-500/10 text-emerald-400` (aprovado), `bg-red-500/10 text-red-400` (reprovado).

---

## Models e status — referência rápida

| Model | App | Choices de status |
|---|---|---|
| `User` | `users` | — |
| `Job` | `hub` | `active`, `paused`, `archived` |
| `Document` | `documents` | `pending`, `reviewing`, `approved`, `rejected` |
| `Analysis` | `brain` | `rag_status`: `pending`, `processing`, `done`, `error` |
| `DocumentChunk` | `brain` | — |

Relacionamentos: `User → Job → Document → DocumentChunk` / `Document → Analysis ← Job`

---

## Rotas principais — referência rápida

| Nome | URL | Protegida |
|---|---|---|
| `landing` | `/` | não |
| `register` | `/cadastro/` | não |
| `login` | `/entrar/` | não |
| `logout` | `/sair/` | — |
| `dashboard` | `/dashboard/` | sim |
| `job-list` | `/vagas/` | sim |
| `job-create` | `/vagas/nova/` | sim |
| `job-update` | `/vagas/<pk>/editar/` | sim |
| `job-archive` | `/vagas/<pk>/arquivar/` | sim |
| `document-list` | `/vagas/<job_pk>/documentos/` | sim |
| `document-upload` | `/vagas/<job_pk>/documentos/upload/` | sim |
| `document-status` | `/documentos/<pk>/status/` | sim |
| `document-delete` | `/documentos/<pk>/excluir/` | sim |
| `job-analysis` | `/vagas/<pk>/analise/` | sim |
| `document-analyze` | `/documentos/<document_pk>/analisar/` | sim |

---

## Pipeline RAG — onde fica

```
brain/services/
├── pdf_extractor.py   → extract_text_from_pdf(), split_into_chunks()
├── vector_store.py    → index_document_chunks(), search_similar_chunks(), delete_document_chunks()
└── rag_pipeline.py    → run_rag_analysis(document_id, job_id)  ← ponto de entrada principal
```

Ao excluir um `Document`, o signal em `documents/signals.py` chama `delete_document_chunks()` automaticamente.

Detalhes em `docs/rag.md`.

---

## O que não fazer

- Não usar aspas duplas em código Python
- Não usar `Job.objects.all()` em views — sempre filtrar por `request.user`
- Não criar views sem `LoginRequiredMixin` para rotas protegidas
- Não escrever signals fora de `signals.py`
- Não hardcodar URLs — usar sempre `reverse_lazy()` ou `{% url %}`
- Não adicionar Docker ou testes automatizados ainda (reservados para sprints finais)
- Não implementar funcionalidades fora do escopo definido no PRD
- Não usar modo claro — o sistema é exclusivamente dark mode
