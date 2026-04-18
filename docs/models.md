# Models

Todos os models possuem os campos `created_at` (preenchido automaticamente na criação) e `updated_at` (atualizado automaticamente a cada save).

---

## User (`users`)

Model customizado que substitui o `User` padrão do Django. O identificador de login é o `email`, não o `username`.

| Campo | Tipo | Descrição |
|---|---|---|
| `email` | `EmailField` (único) | Identificador principal, usado no login |
| `first_name` | `CharField` | Primeiro nome |
| `last_name` | `CharField` | Sobrenome |
| `password` | — | Gerenciado pelo Django (hash bcrypt) |
| `is_active` | `BooleanField` | Padrão `True` |
| `is_staff` | `BooleanField` | Padrão `False` |
| `created_at` | `DateTimeField` | Preenchido na criação |
| `updated_at` | `DateTimeField` | Atualizado a cada save |

**Configuração necessária em `settings.py`:**
```python
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']
```

---

## Job (`hub`)

Representa uma vaga ou processo seletivo. Cada vaga pertence a um usuário.

| Campo | Tipo | Descrição |
|---|---|---|
| `user` | `ForeignKey(User)` | Dono da vaga |
| `title` | `CharField(255)` | Título da vaga (obrigatório) |
| `description` | `TextField` | Descrição e requisitos da vaga |
| `status` | `CharField` | Estado atual da vaga |
| `created_at` | `DateTimeField` | — |
| `updated_at` | `DateTimeField` | — |

**Valores de `status`:**

| Valor | Exibição |
|---|---|
| `active` | Ativa |
| `paused` | Pausada |
| `archived` | Arquivada |

Ordenação padrão: `-created_at` (mais recentes primeiro).

---

## Document (`documents`)

Representa um currículo PDF enviado para uma vaga.

| Campo | Tipo | Descrição |
|---|---|---|
| `job` | `ForeignKey(Job)` | Vaga à qual o documento pertence |
| `candidate_name` | `CharField(255)` | Nome do candidato |
| `candidate_email` | `EmailField` | E-mail do candidato (opcional) |
| `file` | `FileField` | Arquivo PDF (`upload_to='documents/%Y/%m/'`) |
| `status` | `CharField` | Estado do documento na triagem |
| `notes` | `TextField` | Observações do recrutador (opcional) |
| `created_at` | `DateTimeField` | — |
| `updated_at` | `DateTimeField` | — |

**Valores de `status`:**

| Valor | Exibição |
|---|---|
| `pending` | Pendente |
| `reviewing` | Em análise |
| `approved` | Aprovado |
| `rejected` | Reprovado |

Ao excluir um `Document`, um signal `post_delete` remove automaticamente o arquivo físico do servidor e todos os chunks do índice vetorial.

Ordenação padrão: `-created_at`.

---

## Analysis (`brain`)

Armazena o resultado da análise RAG de um documento em relação à sua vaga.

| Campo | Tipo | Descrição |
|---|---|---|
| `job` | `ForeignKey(Job)` | Vaga analisada |
| `document` | `ForeignKey(Document)` | Documento analisado |
| `summary` | `TextField` | Resumo gerado pelo LLM |
| `score` | `IntegerField` | Pontuação de aderência (0–100) |
| `rag_status` | `CharField` | Estado do pipeline RAG |
| `error_message` | `TextField` | Mensagem de erro, se houver |
| `created_at` | `DateTimeField` | — |
| `updated_at` | `DateTimeField` | — |

**Valores de `rag_status`:**

| Valor | Descrição |
|---|---|
| `pending` | Análise ainda não iniciada |
| `processing` | Pipeline em execução |
| `done` | Análise concluída com sucesso |
| `error` | Falha durante o pipeline |

---

## DocumentChunk (`brain`)

Armazena os trechos (chunks) de texto extraídos de um PDF para indexação vetorial.

| Campo | Tipo | Descrição |
|---|---|---|
| `document` | `ForeignKey(Document)` | Documento de origem |
| `chunk_index` | `IntegerField` | Posição do chunk no documento |
| `content` | `TextField` | Texto do trecho |
| `embedding_id` | `CharField` | ID do embedding no ChromaDB |
| `created_at` | `DateTimeField` | — |
| `updated_at` | `DateTimeField` | — |

---

## Diagrama de relacionamentos

```
User ──< Job ──< Document ──< DocumentChunk
                    │
                    └──< Analysis
                              │
                         (pertence também a Job)
```
