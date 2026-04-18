# Índice de Agentes — Crivopy

Esta pasta contém as definições dos agentes de IA especializados para o desenvolvimento do projeto Crivopy. Cada agente possui diretrizes específicas baseadas na stack tecnológica e no PRD.

## Agentes Disponíveis

| Agente | Arquivo | Função | Quando Usar |
|---|---|---|---|
| **Backend Django** | [backend-django.md](./backend-django.md) | Especialista em Python 3.13, Django 5.x e RAG. | Para criar models, views, lógica de negócios, integração com ChromaDB e processamento de PDFs. |
| **Frontend Tailwind** | [frontend-tailwind.md](./frontend-tailwind.md) | Especialista em Django Template Language e TailwindCSS. | Para criar interfaces, componentes, layouts responsivos e garantir a fidelidade ao Design System. |
| **QA & Tester** | [qa-tester.md](./qa-tester.md) | Especialista em testes E2E com Playwright. | Para validar fluxos do sistema, testar bugs, verificar responsividade e conformidade visual. |

## Uso de MCP Servers

- **Context7:** Usado pelos agentes de desenvolvimento (Backend e Frontend) para acessar documentações atualizadas e padrões de código.
- **Playwright:** Usado pelo agente de QA para interagir com a aplicação em execução e validar o comportamento real.

## Instruções Gerais
Ao solicitar uma tarefa para um agente, certifique-se de referenciar o arquivo `.md` correspondente para carregar seu contexto e diretrizes.
