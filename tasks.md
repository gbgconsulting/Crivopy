##  Lista de Tarefas por Sprint

---

### SPRINT 0 — Configuração do Ambiente e Fundação

#### Tarefa 0.1 — Configuração inicial do projeto Django
- [X] **0.1.1** Verificar versão do Python instalada (`python --version`) e confirmar Python 3.13
- [X] **0.1.2** Criar e ativar ambiente virtual (`python -m venv .venv`)
- [X] **0.1.3** Instalar Django (`pip install django`)
- [X] **0.1.4** Confirmar que o projeto Django já existe com a estrutura de diretórios especificada
- [X] **0.1.5** Criar arquivo `requirements.txt` com as dependências iniciais (`Django`, `Pillow`)

#### Tarefa 0.2 — Configuração do `settings.py`
- [X] **0.2.1** Definir `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Sao_Paulo'`
- [X] **0.2.2** Adicionar todas as apps ao `INSTALLED_APPS`: `users`, `hub`, `documents`, `brain`, `chat`
- [X] **0.2.3** Configurar `MEDIA_URL = '/media/'` e `MEDIA_ROOT = BASE_DIR / 'media'`
- [X] **0.2.4** Configurar `STATIC_URL = '/static/'` e `STATICFILES_DIRS`
- [X] **0.2.5** Definir `AUTH_USER_MODEL = 'users.User'`
- [X] **0.2.6** Definir `AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']`
- [X] **0.2.7** Definir `LOGIN_URL`, `LOGIN_REDIRECT_URL` e `LOGOUT_REDIRECT_URL`
- [X] **0.2.8** Configurar `TEMPLATES` com `DIRS` apontando para `templates/` na raiz do projeto
- [X] **0.2.9** Definir `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`

#### Tarefa 0.3 — Estrutura de templates e arquivos estáticos
- [X] **0.3.1** Criar diretório `templates/` na raiz do projeto
- [X] **0.3.2** Criar subdiretórios: `templates/users/`, `templates/hub/`, `templates/documents/`, `templates/brain/`, `templates/public/`
- [X] **0.3.3** Criar diretório `static/` na raiz do projeto
- [X] **0.3.4** Criar arquivo `templates/base.html` com estrutura HTML base, import do TailwindCSS (CDN) e fonte Inter
- [X] **0.3.5** Criar arquivo `templates/partials/_sidebar.html` com navegação autenticada
- [X] **0.3.6** Criar arquivo `templates/partials/_navbar_public.html` para navbar da landing page
- [X] **0.3.7** Criar arquivo `templates/partials/_messages.html` para exibição de mensagens Django

#### Tarefa 0.4 — Configuração do `core/urls.py`
- [X] **0.4.1** Configurar `urlpatterns` raiz incluindo `users.urls`, `hub.urls`, `documents.urls`, `brain.urls`
- [X] **0.4.2** Adicionar rota para a landing page (`/`) apontando para view da app `users` ou `public`
- [X] **0.4.3** Adicionar `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` para servir arquivos de mídia em desenvolvimento

---

### SPRINT 1 — Autenticação e Usuários

#### Tarefa 1.1 — Model de usuário customizado (`users/models.py`)
- [X] **1.1.1** Criar classe `User` herdando de `AbstractBaseUser` e `PermissionsMixin`
- [X] **1.1.2** Definir campo `email` como `EmailField(unique=True)` — identificador principal
- [X] **1.1.3** Definir campos `first_name` e `last_name` como `CharField`
- [X] **1.1.4** Definir campo `is_active` com `default=True`
- [X] **1.1.5** Definir campo `is_staff` com `default=False`
- [X] **1.1.6** Definir campos `created_at = models.DateTimeField(auto_now_add=True)` e `updated_at = models.DateTimeField(auto_now=True)`
- [X] **1.1.7** Definir `USERNAME_FIELD = 'email'` e `REQUIRED_FIELDS = ['first_name', 'last_name']`
- [X] **1.1.8** Criar classe `UserManager` herdando de `BaseUserManager` com métodos `create_user` e `create_superuser`
- [X] **1.1.9** Implementar método `__str__` retornando `self.email`

#### Tarefa 1.2 — Backend de autenticação por e-mail (`users/backends.py`)
- [X] **1.2.1** Criar arquivo `users/backends.py`
- [X] **1.2.2** Criar classe `EmailBackend` herdando de `ModelBackend`
- [X] **1.2.3** Sobrescrever método `authenticate(request, email=None, password=None, **kwargs)`
- [X] **1.2.4** Buscar usuário pelo campo `email` e validar senha com `user.check_password(password)`
- [X] **1.2.5** Retornar `None` se usuário não encontrado ou senha inválida

#### Tarefa 1.3 — Forms de autenticação (`users/forms.py`)
- [X] **1.3.1** Criar arquivo `users/forms.py`
- [X] **1.3.2** Criar `RegisterForm` herdando de `forms.ModelForm` com campos `first_name`, `last_name`, `email`, `password`, `password_confirm`
- [X] **1.3.3** Implementar validação de `clean_password_confirm` verificando se senhas conferem
- [X] **1.3.4** Implementar `save(commit=True)` chamando `set_password` para hash seguro
- [X] **1.3.5** Criar `LoginForm` herdando de `forms.Form` com campos `email` e `password`
- [X] **1.3.6** Adicionar classes CSS do design system em cada widget dos forms via `attrs`

#### Tarefa 1.4 — Views de autenticação (`users/views.py`)
- [X] **1.4.1** Criar `RegisterView` como `FormView` com `form_class = RegisterForm`
- [X] **1.4.2** Implementar `form_valid` salvando o usuário e redirecionando para login com `messages.success`
- [X] **1.4.3** Criar `LoginView` como `FormView` com `form_class = LoginForm`
- [X] **1.4.4** Implementar `form_valid` chamando `authenticate` e `login` do Django
- [X] **1.4.5** Redirecionar para dashboard em caso de sucesso; retornar erro no form em caso de falha
- [X] **1.4.6** Criar `LogoutView` como `View` com método `post` chamando `logout` e redirecionando para `/`
- [X] **1.4.7** Criar `LandingPageView` como `TemplateView` com `template_name = 'public/landing.html'`

#### Tarefa 1.5 — URLs de usuários (`users/urls.py`)
- [X] **1.5.1** Criar arquivo `users/urls.py`
- [X] **1.5.2** Definir rota `''` para `LandingPageView` com nome `landing`
- [X] **1.5.3** Definir rota `'cadastro/'` para `RegisterView` com nome `register`
- [X] **1.5.4** Definir rota `'entrar/'` para `LoginView` com nome `login`
- [X] **1.5.5** Definir rota `'sair/'` para `LogoutView` com nome `logout`

#### Tarefa 1.6 — Templates de autenticação
- [X] **1.6.1** Criar `templates/public/landing.html` com seção hero, gradiente, botões "Cadastre-se" e "Entrar", e apresentação do produto
- [X] **1.6.2** Criar `templates/users/register.html` com formulário de cadastro centralizado, design dark, logo Crivopy e link para login
- [X] **1.6.3** Criar `templates/users/login.html` com formulário de login centralizado, design dark, logo Crivopy e link para cadastro
- [X] **1.6.4** Garantir que mensagens Django (`{% if messages %}`) sejam renderizadas em todos os templates

#### Tarefa 1.7 — Admin (`users/admin.py`)
- [X] **1.7.1** Registrar model `User` no admin com `UserAdmin` customizado
- [X] **1.7.2** Configurar `list_display = ['email', 'first_name', 'last_name', 'is_active', 'created_at']`

#### Tarefa 1.8 — Migrations e validação
- [X] **1.8.1** Executar `python manage.py makemigrations users`
- [X] **1.8.2** Executar `python manage.py migrate`
- [X] **1.8.3** Criar superusuário de teste com `python manage.py createsuperuser`
- [X] **1.8.4** Testar cadastro, login e logout manualmente no browser
- [X] **1.8.5** Verificar que rotas protegidas redirecionam para `/entrar/` quando não autenticado

---

### SPRINT 2 — Dashboard e Estrutura Autenticada

#### Tarefa 2.1 — Template base autenticado
- [X] **2.1.1** Criar `templates/base_authenticated.html` herdando de `base.html` com layout sidebar + conteúdo
- [X] **2.1.2** Incluir `{% include 'partials/_sidebar.html' %}` no layout
- [X] **2.1.3** Sidebar deve conter: logo Crivopy, links de navegação (Dashboard, Vagas, Documentos, Análises), informações do usuário logado e botão de logout
- [X] **2.1.4** Adicionar indicador visual de item ativo na sidebar usando template tags do Django (`{% url %}` comparado a `request.path`)
- [X] **2.1.5** Tornar o layout responsivo: sidebar colapsável via checkbox CSS ou `hidden md:flex`

#### Tarefa 2.2 — Dashboard view e template
- [X] **2.2.1** Criar view `DashboardView` como `LoginRequiredMixin` + `TemplateView` na app `hub`
- [X] **2.2.2** Sobrescrever `get_context_data` para injetar contagem de vagas ativas, total de documentos e documentos pendentes do usuário logado
- [X] **2.2.3** Criar rota `'dashboard/'` em `hub/urls.py` com nome `dashboard`
- [X] **2.2.4** Criar `templates/hub/dashboard.html` herdando de `base_authenticated.html`
- [X] **2.2.5** Exibir cards de resumo com métricas (vagas ativas, documentos enviados, pendentes, aprovados)
- [X] **2.2.6** Design dos cards: gradiente sutil, ícone representativo, número em destaque, label descritiva

#### Tarefa 2.3 — Proteção de rotas
- [X] **2.3.1** Confirmar que `LoginRequiredMixin` está aplicado em todas as views autenticadas
- [X] **2.3.2** Verificar que `settings.LOGIN_URL` aponta para a view de login correta
- [X] **2.3.3** Testar acesso direto a `/dashboard/` sem autenticação e confirmar redirecionamento

---

### SPRINT 3 — Gestão de Vagas (hub)

#### Tarefa 3.1 — Model de Vaga (`hub/models.py`)
- [X] **3.1.1** Criar classe `Job` herdando de `models.Model`
- [X] **3.1.2** Definir `user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')`
- [X] **3.1.3** Definir `title = models.CharField(max_length=255)`
- [X] **3.1.4** Definir `description = models.TextField(blank=True)`
- [X] **3.1.5** Definir constantes de status: `ACTIVE`, `PAUSED`, `ARCHIVED` e campo `status = models.CharField(choices=..., default=ACTIVE)`
- [X] **3.1.6** Definir `created_at` e `updated_at` com `auto_now_add` e `auto_now`
- [X] **3.1.7** Implementar `__str__` retornando `self.title`
- [X] **3.1.8** Adicionar `class Meta` com `ordering = ['-created_at']`

#### Tarefa 3.2 — Form de Vaga (`hub/forms.py`)
- [X] **3.2.1** Criar arquivo `hub/forms.py`
- [X] **3.2.2** Criar `JobForm` como `ModelForm` com campos `title`, `description`, `status`
- [X] **3.2.3** Aplicar classes CSS do design system nos widgets

#### Tarefa 3.3 — Views de Vaga (`hub/views.py`)
- [X] **3.3.1** Criar `JobListView` como `LoginRequiredMixin` + `ListView` com `model = Job` e `template_name = 'hub/job_list.html'`
- [X] **3.3.2** Sobrescrever `get_queryset` para filtrar apenas vagas do `request.user`
- [X] **3.3.3** Criar `JobCreateView` como `LoginRequiredMixin` + `CreateView` com `form_class = JobForm`
- [X] **3.3.4** Sobrescrever `form_valid` para setar `form.instance.user = self.request.user`
- [X] **3.3.5** Criar `JobUpdateView` como `LoginRequiredMixin` + `UpdateView` com `form_class = JobForm`
- [X] **3.3.6** Sobrescrever `get_queryset` para garantir que o usuário só edita suas próprias vagas
- [X] **3.3.7** Criar `JobArchiveView` como `LoginRequiredMixin` + `View` com método `post` alterando status para `archived`
- [X] **3.3.8** Adicionar `messages.success` em todas as ações de criação, edição e arquivamento

#### Tarefa 3.4 — URLs de Vaga (`hub/urls.py`)
- [X] **3.4.1** Criar arquivo `hub/urls.py`
- [X] **3.4.2** Rota `'vagas/'` → `JobListView` → nome `job-list`
- [X] **3.4.3** Rota `'vagas/nova/'` → `JobCreateView` → nome `job-create`
- [X] **3.4.4** Rota `'vagas/<int:pk>/editar/'` → `JobUpdateView` → nome `job-update`
- [X] **3.4.5** Rota `'vagas/<int:pk>/arquivar/'` → `JobArchiveView` → nome `job-archive`

#### Tarefa 3.5 — Templates de Vaga
- [X] **3.5.1** Criar `templates/hub/job_list.html` com tabela ou grid de cards de vagas, badge de status colorido e botões de ação
- [X] **3.5.2** Criar `templates/hub/job_form.html` reutilizável para criação e edição de vaga
- [X] **3.5.3** Adicionar mensagem de estado vazio quando não há vagas cadastradas
- [X] **3.5.4** Adicionar botão "Nova Vaga" em destaque na listagem

#### Tarefa 3.6 — Admin (`hub/admin.py`)
- [X] **3.6.1** Registrar model `Job` no admin
- [X] **3.6.2** Configurar `list_display = ['title', 'user', 'status', 'created_at']`
- [X] **3.6.3** Adicionar `list_filter = ['status']` e `search_fields = ['title']`

#### Tarefa 3.7 — Migrations
- [X] **3.7.1** Executar `python manage.py makemigrations hub`
- [X] **3.7.2** Executar `python manage.py migrate`
- [X] **3.7.3** Testar CRUD de vagas manualmente

---

### SPRINT 4 — Gestão de Documentos

#### Tarefa 4.1 — Model de Documento (`documents/models.py`)
- [X] **4.1.1** Criar classe `Document` herdando de `models.Model`
- [X] **4.1.2** Definir `job = models.ForeignKey('hub.Job', on_delete=models.CASCADE, related_name='documents')`
- [X] **4.1.3** Definir `candidate_name = models.CharField(max_length=255)`
- [X] **4.1.4** Definir `candidate_email = models.EmailField(blank=True)`
- [X] **4.1.5** Definir `file = models.FileField(upload_to='documents/%Y/%m/')` — organiza por ano/mês
- [X] **4.1.6** Definir constantes de status: `PENDING`, `REVIEWING`, `APPROVED`, `REJECTED` e campo `status`
- [X] **4.1.7** Definir `notes = models.TextField(blank=True)`
- [X] **4.1.8** Definir `created_at` e `updated_at`
- [X] **4.1.9** Implementar `__str__` retornando `self.candidate_name`
- [X] **4.1.10** Adicionar `class Meta` com `ordering = ['-created_at']`

#### Tarefa 4.2 — Signals para limpeza de arquivo (`documents/signals.py`)
- [X] **4.2.1** Criar arquivo `documents/signals.py`
- [X] **4.2.2** Implementar signal `post_delete` no model `Document` para remover o arquivo físico do servidor quando o registro é deletado
- [X] **4.2.3** Conectar o signal no `documents/apps.py` dentro do método `ready()`

#### Tarefa 4.3 — Form de Documento (`documents/forms.py`)
- [X] **4.3.1** Criar arquivo `documents/forms.py`
- [X] **4.3.2** Criar `DocumentUploadForm` como `ModelForm` com campos `candidate_name`, `candidate_email`, `file`, `notes`
- [X] **4.3.3** Implementar validação do campo `file` para aceitar apenas arquivos com extensão `.pdf` e tipo MIME `application/pdf`
- [X] **4.3.4** Aplicar classes CSS do design system nos widgets
- [X] **4.3.5** Criar `DocumentStatusForm` como `ModelForm` apenas com o campo `status`

#### Tarefa 4.4 — Views de Documento (`documents/views.py`)
- [X] **4.4.1** Criar `DocumentListView` como `LoginRequiredMixin` + `ListView` filtrada por `job_id` da URL e validando que a vaga pertence ao `request.user`
- [X] **4.4.2** Injetar objeto `job` no contexto para exibir título da vaga no template
- [X] **4.4.3** Criar `DocumentUploadView` como `LoginRequiredMixin` + `CreateView` com `form_class = DocumentUploadForm`
- [X] **4.4.4** Sobrescrever `form_valid` para setar `form.instance.job_id` a partir do `pk` da URL
- [X] **4.4.5** Validar que o `job` pertence ao `request.user` antes de permitir upload
- [X] **4.4.6** Criar `DocumentStatusUpdateView` como `LoginRequiredMixin` + `UpdateView` com `form_class = DocumentStatusForm`
- [X] **4.4.7** Validar que o documento pertence a uma vaga do `request.user`
- [X] **4.4.8** Criar `DocumentDeleteView` como `LoginRequiredMixin` + `DeleteView`
- [X] **4.4.9** Sobrescrever `get_queryset` para segurança — apenas documentos de vagas do usuário

#### Tarefa 4.5 — URLs de Documento (`documents/urls.py`)
- [X] **4.5.1** Criar arquivo `documents/urls.py`
- [X] **4.5.2** Rota `'vagas/<int:job_pk>/documentos/'` → `DocumentListView` → nome `document-list`
- [X] **4.5.3** Rota `'vagas/<int:job_pk>/documentos/upload/'` → `DocumentUploadView` → nome `document-upload`
- [X] **4.5.4** Rota `'documentos/<int:pk>/status/'` → `DocumentStatusUpdateView` → nome `document-status`
- [X] **4.5.5** Rota `'documentos/<int:pk>/excluir/'` → `DocumentDeleteView` → nome `document-delete`

#### Tarefa 4.6 — Templates de Documento
- [X] **4.6.1** Criar `templates/documents/document_list.html` com listagem de documentos em tabela ou cards, exibindo nome, e-mail, status badge e data
- [X] **4.6.2** Adicionar link para download/visualização do PDF em nova aba
- [X] **4.6.3** Criar `templates/documents/document_upload.html` com formulário de upload com área de drag-and-drop visual (CSS only)
- [X] **4.6.4** Criar `templates/documents/document_confirm_delete.html` com mensagem de confirmação e botões de cancelar/confirmar
- [X] **4.6.5** Criar `templates/documents/document_status_form.html` com select de status

#### Tarefa 4.7 — Admin (`documents/admin.py`)
- [X] **4.7.1** Registrar model `Document` no admin
- [X] **4.7.2** Configurar `list_display`, `list_filter` por status e `search_fields` por nome do candidato

#### Tarefa 4.8 — Migrations
- [X] **4.8.1** Executar `python manage.py makemigrations documents`
- [X] **4.8.2** Executar `python manage.py migrate`
- [X] **4.8.3** Testar upload, listagem, mudança de status e exclusão manualmente

---

### SPRINT 5 — Módulo de Análise (brain)

#### Tarefa 5.1 — Model de Análise (`brain/models.py`)
- [X] **5.1.1** Criar classe `Analysis` herdando de `models.Model`
- [X] **5.1.2** Definir `job = models.ForeignKey('hub.Job', on_delete=models.CASCADE, related_name='analyses')`
- [X] **5.1.3** Definir `document = models.ForeignKey('documents.Document', on_delete=models.CASCADE, related_name='analyses')`
- [X] **5.1.4** Definir `summary = models.TextField(blank=True)`
- [X] **5.1.5** Definir `score = models.IntegerField(null=True, blank=True)` — pontuação 0-100 para uso futuro
- [X] **5.1.6** Definir `created_at` e `updated_at`

#### Tarefa 5.2 — Painel de Análise por Vaga (`brain/views.py`)
- [X] **5.2.1** Criar `JobAnalysisView` como `LoginRequiredMixin` + `DetailView` com model `Job`
- [X] **5.2.2** Sobrescrever `get_queryset` para filtrar apenas vagas do `request.user`
- [X] **5.2.3** Sobrescrever `get_context_data` para injetar contagem de documentos agrupados por status usando `documents.values('status').annotate(count=Count('id'))`
- [X] **5.2.4** Injetar lista dos documentos aprovados e em análise no contexto

#### Tarefa 5.3 — URLs de Análise (`brain/urls.py`)
- [X] **5.3.1** Criar arquivo `brain/urls.py`
- [X] **5.3.2** Rota `'vagas/<int:pk>/analise/'` → `JobAnalysisView` → nome `job-analysis`

#### Tarefa 5.4 — Template de Análise
- [X] **5.4.1** Criar `templates/brain/job_analysis.html` herdando de `base_authenticated.html`
- [X] **5.4.2** Exibir título da vaga e cards de contagem por status (Pendentes, Em análise, Aprovados, Reprovados)
- [X] **5.4.3** Exibir tabela ou lista dos documentos aprovados em destaque

#### Tarefa 5.5 — Admin (`brain/admin.py`)
- [X] **5.5.1** Registrar model `Analysis` no admin

#### Tarefa 5.6 — Migrations
- [X] **5.6.1** Executar `python manage.py makemigrations brain`
- [X] **5.6.2** Executar `python manage.py migrate`

---

### SPRINT 5B — Pipeline RAG (brain)

#### Tarefa 5B.1 — Dependências RAG
- [X] **5B.1.1** Adicionar ao `requirements.txt`: `pymupdf` (ou `pdfplumber`), `sentence-transformers`, `chromadb`, `langchain` (opcional), `openai` (opcional)
- [X] **5B.1.2** Executar `pip install` das novas dependências e confirmar sem conflitos
- [X] **5B.1.3** Definir no `settings.py` as configurações do RAG: `CHROMA_DB_PATH = BASE_DIR / 'chroma_db'`, `LLM_PROVIDER` e `OPENAI_API_KEY` (via variável de ambiente)

#### Tarefa 5B.2 — Serviço de extração de texto (`brain/services/pdf_extractor.py`)
- [X] **5B.2.1** Criar diretório `brain/services/` com arquivo `__init__.py`
- [X] **5B.2.2** Criar arquivo `brain/services/pdf_extractor.py`
- [X] **5B.2.3** Implementar função `extract_text_from_pdf(file_path: str) -> str` usando PyMuPDF (`fitz.open`)
- [X] **5B.2.4** Implementar função `split_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]` para dividir o texto em chunks com sobreposição
- [X] **5B.2.5** Tratar exceção para PDFs baseados em imagem (texto vazio) retornando string vazia e logando aviso

#### Tarefa 5B.3 — Serviço de embeddings e índice vetorial (`brain/services/vector_store.py`)
- [X] **5B.3.1** Criar arquivo `brain/services/vector_store.py`
- [X] **5B.3.2** Inicializar cliente ChromaDB persistido em `settings.CHROMA_DB_PATH`
- [X] **5B.3.3** Implementar função `get_or_create_collection(collection_name: str)` retornando coleção ChromaDB
- [X] **5B.3.4** Implementar função `index_document_chunks(document_id: int, chunks: list[str])` gerando embeddings com Sentence Transformers e adicionando ao ChromaDB com metadado `document_id`
- [X] **5B.3.5** Implementar função `search_similar_chunks(query: str, document_id: int, n_results: int = 5) -> list[str]` buscando chunks semanticamente similares filtrando pelo `document_id`
- [X] **5B.3.6** Implementar função `delete_document_chunks(document_id: int)` removendo todos os chunks de um documento do índice

#### Tarefa 5B.4 — Serviço de geração de análise (`brain/services/rag_pipeline.py`)
- [X] **5B.4.1** Criar arquivo `brain/services/rag_pipeline.py`
- [X] **5B.4.2** Implementar função `build_prompt(job_description: str, relevant_chunks: list[str]) -> str` montando o prompt com os requisitos da vaga e os trechos relevantes do currículo
- [X] **5B.4.3** Implementar função `call_llm(prompt: str) -> str` chamando a API OpenAI (GPT-4o-mini) ou modelo local, retornando texto gerado
- [X] **5B.4.4** Implementar função `parse_llm_response(response: str) -> dict` extraindo `summary` e `score` (0–100) do texto retornado pelo LLM (usar formato JSON estruturado no prompt)
- [X] **5B.4.5** Implementar função principal `run_rag_analysis(document_id: int, job_id: int) -> dict` orquestrando todo o pipeline: extração → chunking → indexação → busca → geração → parse → retorno

#### Tarefa 5B.5 — Integração do RAG ao model Analysis (`brain/models.py`)
- [X] **5B.5.1** Confirmar que `Analysis` possui campos `summary`, `score`, `created_at` e `updated_at` suficientes para armazenar o resultado RAG
- [X] **5B.5.2** Adicionar campo `rag_status = models.CharField(choices=[...], default='pending')` com estados: `pending`, `processing`, `done`, `error`
- [X] **5B.5.3** Adicionar campo `error_message = models.TextField(blank=True)` para registrar falhas do pipeline

#### Tarefa 5B.6 — Model DocumentChunk (`brain/models.py`)
- [X] **5B.6.1** Criar classe `DocumentChunk` com `document` (FK), `chunk_index` (int), `content` (TextField), `embedding_id` (CharField — ID no ChromaDB), `created_at`, `updated_at`
- [X] **5B.6.2** Executar `python manage.py makemigrations brain` e `migrate`

#### Tarefa 5B.7 — Signal para limpeza de chunks ao excluir documento (`documents/signals.py`)
- [x] **5B.7.1** Adicionar ao `documents/signals.py` um signal `post_delete` que chama `delete_document_chunks(document_id)` do `vector_store` ao excluir um `Document`
- [x] **5B.7.2** Garantir que o signal está conectado no `documents/apps.py`

#### Tarefa 5B.8 — View para acionar análise RAG (`brain/views.py`)
- [x] **5B.8.1** Criar `DocumentAnalysisView` como `LoginRequiredMixin` + `View` com método `post`
- [x] **5B.8.2** Receber `document_id` da URL, validar que pertence a uma vaga do `request.user`
- [x] **5B.8.3** Criar ou atualizar registro `Analysis` com `rag_status = 'processing'`
- [x] **5B.8.4** Chamar `run_rag_analysis(document_id, job_id)` e salvar resultado no `Analysis`
- [x] **5B.8.5** Atualizar `rag_status` para `done` em caso de sucesso ou `error` em caso de exceção, salvando `error_message`
- [x] **5B.8.6** Redirecionar para página de detalhe/listagem com mensagem de sucesso ou erro

#### Tarefa 5B.9 — Rota para análise RAG (`brain/urls.py`)
- [x] **5B.9.1** Adicionar rota `'documentos/<int:document_pk>/analisar/'` → `DocumentAnalysisView` → nome `document-analyze`

#### Tarefa 5B.10 — Exibição do resultado RAG nos templates
- [x] **5B.10.1** Na listagem de documentos (`document_list.html`), adicionar botão "Analisar com IA" por documento
- [x] **5B.10.2** Exibir score como barra de progresso visual (div com largura proporcional ao score, colorida por faixa: vermelho < 40, amarelo 40–70, verde > 70)
- [x] **5B.10.3** Exibir o campo `summary` do `Analysis` em um bloco colapsável ou card abaixo do documento
- [x] **5B.10.4** Exibir `rag_status` como badge (Pendente, Processando, Concluído, Erro)
- [x] **5B.10.5** Atualizar template de análise por vaga (`job_analysis.html`) para incluir ranking de candidatos por score RAG

---

### SPRINT 6 — Refinamentos de UI e Ajustes Finais

#### Tarefa 6.1 — Refinamento do Design System
- [ ] **6.1.1** Revisar todos os templates e garantir consistência visual com o design system definido
- [ ] **6.1.2** Garantir que todos os badges de status usam as cores corretas do design system
- [ ] **6.1.3** Revisar responsividade em todos os templates (mobile, tablet, desktop)
- [ ] **6.1.4** Adicionar transições CSS (`transition-all duration-200`) em todos os elementos interativos
- [ ] **6.1.5** Verificar acessibilidade básica: labels associados a inputs, contraste de cores mínimo

#### Tarefa 6.2 — Mensagens e Feedbacks
- [ ] **6.2.1** Garantir que mensagens Django (`messages.success`, `messages.error`) são exibidas em todas as ações
- [ ] **6.2.2** Estilizar o partial `_messages.html` com alertas coloridos e ícones correspondentes ao tipo (sucesso, erro, aviso)
- [ ] **6.2.3** Adicionar estados vazios ("Nenhuma vaga cadastrada", "Nenhum documento enviado") com ilustração ou ícone

#### Tarefa 6.3 — Segurança e Validações
- [ ] **6.3.1** Confirmar que `{% csrf_token %}` está em todos os formulários POST
- [ ] **6.3.2** Confirmar que nenhum endpoint permite acesso a dados de outro usuário
- [ ] **6.3.3** Definir `FILE_UPLOAD_MAX_MEMORY_SIZE` e `DATA_UPLOAD_MAX_MEMORY_SIZE` no `settings.py` para limitar tamanho de upload
- [ ] **6.3.4** Adicionar `MAX_UPLOAD_SIZE` customizado e validar no form

#### Tarefa 6.4 — Estrutura do módulo Chat
- [ ] **6.4.1** Criar model placeholder `ChatMessage` em `chat/models.py` com `created_at` e `updated_at` (sem funcionalidade ainda)
- [ ] **6.4.2** Registrar no admin para fins de visibilidade futura

#### Tarefa 6.5 — Documentação do projeto
- [ ] **6.5.1** Criar `README.md` na raiz do projeto com instrução de setup (`git clone`, `venv`, `pip install`, `migrate`, `runserver`)
- [ ] **6.5.2** Documentar variáveis de ambiente importantes
- [ ] **6.5.3** Documentar estrutura de apps e responsabilidades de cada uma

---

### SPRINT FINAL A — Docker (futura)
- [ ] **A.1** Criar `Dockerfile` para a aplicação Django
- [ ] **A.2** Criar `docker-compose.yml` com serviço web
- [ ] **A.3** Configurar variáveis de ambiente via `.env`
- [ ] **A.4** Testar build e execução do container

### SPRINT FINAL B — Testes Automatizados (futura)
- [ ] **B.1** Configurar `pytest-django` ou Django TestCase
- [ ] **B.2** Escrever testes unitários para models (`User`, `Job`, `Document`)
- [ ] **B.3** Escrever testes de integração para views de autenticação
- [ ] **B.4** Escrever testes de integração para CRUD de vagas e documentos
- [ ] **B.5** Configurar GitHub Actions para CI

---