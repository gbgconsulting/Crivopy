# Documentação — Crivopy

Sistema de triagem de currículos e documentos PDF com suporte a análise via IA (RAG).

---

## Índice

| Arquivo | Conteúdo |
|---|---|
| [arquitetura.md](./arquitetura.md) | Visão geral do projeto, stack, estrutura de apps e fluxo de dados |
| [models.md](./models.md) | Descrição de todos os models, campos, relacionamentos e valores de status |
| [urls.md](./urls.md) | Mapa completo de rotas do sistema |
| [design-system.md](./design-system.md) | Paleta de cores, tipografia, componentes e padrões de UI |
| [codigo.md](./codigo.md) | Convenções de código, padrões de views, forms, signals e segurança |
| [rag.md](./rag.md) | Como funciona o pipeline de análise com IA (RAG) |

---

## Setup rápido

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd Crivopy

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Aplicar migrações
python manage.py migrate

# 5. Criar superusuário
python manage.py createsuperuser

# 6. Rodar o servidor
python manage.py runserver
```

O sistema estará disponível em `http://127.0.0.1:8000/`.

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua-secret-key-aqui
DEBUG=True
OPENAI_API_KEY=sua-chave-openai  # necessário para o módulo RAG
```

> Para desenvolvimento, o sistema funciona sem `OPENAI_API_KEY` exceto pelo módulo de análise RAG.
