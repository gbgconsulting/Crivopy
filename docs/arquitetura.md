# Arquitetura

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.13 |
| Framework Web | Django 5.x |
| Banco de Dados | SQLite (padrão Django) |
| Frontend | Django Template Language + TailwindCSS (via CDN) |
| Autenticação | Django Auth com backend customizado (login por e-mail) |
| Armazenamento de arquivos | Sistema de arquivos local (`MEDIA_ROOT`) |
| Extração de texto PDF | PyMuPDF (`fitz`) |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`, modelo local) |
| Banco vetorial | ChromaDB (persistido em disco local) |
| LLM | API OpenAI (GPT-4o-mini) |
| Servidor de desenvolvimento | Django `runserver` |

---

## Estrutura de diretórios

```
Crivopy/
│
├── core/               → Configurações do projeto (settings, urls raiz, wsgi, asgi)
├── users/              → Model de usuário customizado e autenticação por e-mail
├── hub/                → Gestão de vagas (Job)
├── documents/          → Upload e gestão de currículos PDF (Document)
├── brain/              → Análise dos documentos e pipeline RAG (Analysis, DocumentChunk)
├── chat/               → Estrutura base reservada para uso futuro
│
├── templates/          → Todos os templates HTML do projeto
│   ├── base.html
│   ├── base_authenticated.html
│   ├── partials/
│   ├── public/
│   ├── users/
│   ├── hub/
│   ├── documents/
│   └── brain/
│
├── static/             → Arquivos estáticos (CSS, JS, imagens)
├── media/              → Arquivos enviados pelos usuários (currículos PDF)
├── chroma_db/          → Índice vetorial do ChromaDB (gerado em tempo de execução)
└── docs/               → Esta documentação
```

---

## Responsabilidade de cada app

**`core`** — configurações centrais. Não contém models nem views de negócio. O `urls.py` raiz inclui as rotas de todas as outras apps.

**`users`** — model `User` customizado com login por e-mail, backend de autenticação (`EmailBackend`), views e forms de cadastro e login.

**`hub`** — model `Job` (vaga). Cada vaga pertence a um usuário e é o ponto de agregação de documentos e análises.

**`documents`** — model `Document` (currículo). Cada documento é um PDF vinculado a uma vaga, com nome do candidato, status e notas.

**`brain`** — models `Analysis` e `DocumentChunk`. Contém o pipeline RAG dividido em serviços (`brain/services/`): extração de texto, geração de embeddings, busca vetorial e chamada ao LLM.

**`chat`** — placeholder. Model `ChatMessage` criado mas sem funcionalidade ativa.

---

## Fluxo de autenticação

1. Visitante acessa a landing page (`/`)
2. Clica em "Cadastre-se" ou "Entrar"
3. Após login bem-sucedido, é redirecionado para o dashboard (`/dashboard/`)
4. Todas as rotas protegidas usam `LoginRequiredMixin`; sem sessão ativa, o usuário é redirecionado para `/entrar/`

---

## Fluxo principal do sistema

```
Usuário cria uma Vaga (Job)
    └── Faz upload de Documentos PDF vinculados à vaga
            └── Altera o status de cada documento manualmente
            └── Aciona a análise RAG por documento
                    └── Pipeline extrai texto → gera embeddings → busca semântica → LLM
                    └── Resultado (resumo + score) salvo em Analysis
                    └── Painel de análise exibe ranking dos candidatos por score
```
