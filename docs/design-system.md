# Design System

O Crivopy usa **dark mode** como padrão único, com gradientes em índigo e violeta. Toda a estilização é feita com classes do TailwindCSS (via CDN) dentro do Django Template Language.

---

## Identidade Visual

- **Tema:** dark mode refinado
- **Cores dominantes:** índigo (`indigo`) e violeta (`violet`)
- **Superfícies:** tons de cinza escuro (`gray-950`, `gray-900`, `gray-800`)
- **Fonte:** Inter (Google Fonts)

---

## Paleta de Cores

| Token | Classe Tailwind | Onde usar |
|---|---|---|
| Fundo da página | `bg-gray-950` | `<body>`, páginas |
| Fundo de card | `bg-gray-900` | Cards, painéis, sidebar |
| Fundo elevado | `bg-gray-800` | Inputs, selects, dropdowns |
| Borda padrão | `border-gray-700` | Divisores, bordas de card |
| Borda sutil | `border-gray-800` | Separadores internos |
| Gradiente primário | `from-indigo-600 to-violet-600` | Botões primários, destaques |
| Gradiente hero | `from-indigo-900 via-gray-950 to-violet-900` | Seção hero da landing page |
| Acento ativo | `text-indigo-400` | Links ativos, labels de destaque |
| Acento hover | `text-violet-400` | Estados de hover |
| Texto principal | `text-gray-100` | Títulos, corpo principal |
| Texto secundário | `text-gray-400` | Labels, legendas, metadados |
| Sucesso | `text-emerald-400` / `bg-emerald-500/10` | Status "Aprovado" |
| Alerta | `text-amber-400` / `bg-amber-500/10` | Status "Em análise" |
| Erro / Perigo | `text-red-400` / `bg-red-500/10` | Status "Reprovado", ações destrutivas |
| Info | `text-blue-400` / `bg-blue-500/10` | Status "Pendente" |

---

## Tipografia

A fonte Inter é importada no `base.html` via Google Fonts e aplicada globalmente.

| Uso | Classes Tailwind |
|---|---|
| Título principal (hero) | `text-4xl font-bold tracking-tight text-gray-100` |
| Título de seção | `text-2xl font-semibold text-gray-100` |
| Subtítulo | `text-lg font-medium text-gray-200` |
| Corpo de texto | `text-base text-gray-300 leading-relaxed` |
| Label / metadado | `text-sm text-gray-400` |
| Badge / chip | `text-xs font-semibold uppercase tracking-wider` |

---

## Botões

### Primário
Usado para a ação principal da tela (salvar, criar, confirmar).

```html
<button class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl
               bg-gradient-to-r from-indigo-600 to-violet-600
               text-white font-semibold text-sm
               hover:from-indigo-500 hover:to-violet-500
               focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-950
               transition-all duration-200 shadow-lg shadow-indigo-900/40">
  Salvar
</button>
```

### Secundário
Usado para ações alternativas (cancelar, voltar, editar).

```html
<button class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl
               bg-gray-800 border border-gray-700
               text-gray-200 font-semibold text-sm
               hover:bg-gray-700 hover:border-gray-600
               focus:outline-none focus:ring-2 focus:ring-gray-500
               transition-all duration-200">
  Cancelar
</button>
```

### Perigo
Usado para ações destrutivas (excluir, remover).

```html
<button class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl
               bg-red-600/20 border border-red-500/30
               text-red-400 font-semibold text-sm
               hover:bg-red-600/30 hover:border-red-500/50
               transition-all duration-200">
  Excluir
</button>
```

---

## Inputs e Forms

### Label

```html
<label class="block text-sm font-medium text-gray-300 mb-1.5">
  Nome do campo
</label>
```

### Input de texto

```html
<input type="text"
       class="w-full px-4 py-2.5 rounded-xl
              bg-gray-800 border border-gray-700
              text-gray-100 placeholder-gray-500
              focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
              transition-all duration-200">
```

### Select

```html
<select class="w-full px-4 py-2.5 rounded-xl
               bg-gray-800 border border-gray-700
               text-gray-100
               focus:outline-none focus:ring-2 focus:ring-indigo-500
               transition-all duration-200">
```

### Textarea

```html
<textarea class="w-full px-4 py-2.5 rounded-xl
                 bg-gray-800 border border-gray-700
                 text-gray-100 placeholder-gray-500
                 focus:outline-none focus:ring-2 focus:ring-indigo-500
                 resize-none transition-all duration-200">
```

### Mensagem de erro inline

```html
<p class="mt-1.5 text-sm text-red-400">Mensagem de erro aqui.</p>
```

---

## Cards

```html
<div class="bg-gray-900 border border-gray-800 rounded-2xl p-6
            hover:border-gray-700 transition-all duration-200
            shadow-xl shadow-black/20">
  <!-- conteúdo do card -->
</div>
```

---

## Badges de Status

Os badges seguem o padrão: fundo com opacidade (`/10`), borda com opacidade (`/20`) e texto colorido.

```html
<!-- Pendente -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full
             text-xs font-semibold
             bg-blue-500/10 text-blue-400 border border-blue-500/20">
  Pendente
</span>

<!-- Em análise -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full
             text-xs font-semibold
             bg-amber-500/10 text-amber-400 border border-amber-500/20">
  Em análise
</span>

<!-- Aprovado -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full
             text-xs font-semibold
             bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
  Aprovado
</span>

<!-- Reprovado -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full
             text-xs font-semibold
             bg-red-500/10 text-red-400 border border-red-500/20">
  Reprovado
</span>
```

---

## Layout e Grid

| Uso | Classes Tailwind |
|---|---|
| Container principal | `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8` |
| Grid de cards (listagens) | `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6` |
| Grid de métricas (dashboard) | `grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4` |
| Layout com sidebar | `flex min-h-screen` — sidebar `w-64`, conteúdo `flex-1` |

---

## Sidebar (área autenticada)

```html
<aside class="w-64 bg-gray-900 border-r border-gray-800 min-h-screen flex flex-col">

  <div class="p-6 border-b border-gray-800">
    <span class="text-xl font-bold bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">
      Crivopy
    </span>
  </div>

  <nav class="flex-1 p-4 space-y-1">

    <!-- Link normal -->
    <a href="{% url 'dashboard' %}"
       class="flex items-center gap-3 px-3 py-2.5 rounded-xl
              text-gray-300 hover:text-white hover:bg-gray-800
              transition-all duration-150 text-sm font-medium">
      Dashboard
    </a>

    <!-- Link ativo -->
    <a href="{% url 'job-list' %}"
       class="flex items-center gap-3 px-3 py-2.5 rounded-xl
              text-white bg-indigo-600/20 border border-indigo-500/30
              text-sm font-medium">
      Vagas
    </a>

  </nav>
</aside>
```

---

## Hierarquia de templates

```
base.html                      ← HTML base, TailwindCSS CDN, fonte Inter
└── base_authenticated.html    ← Layout com sidebar, para todas as páginas autenticadas
    ├── hub/dashboard.html
    ├── hub/job_list.html
    ├── hub/job_form.html
    ├── documents/document_list.html
    ├── documents/document_upload.html
    └── brain/job_analysis.html

templates/public/landing.html  ← Herda de base.html, sem sidebar
templates/users/login.html     ← Herda de base.html, sem sidebar
templates/users/register.html  ← Herda de base.html, sem sidebar
```

### Partials reutilizáveis

| Arquivo | Uso |
|---|---|
| `partials/_sidebar.html` | Navegação lateral da área autenticada |
| `partials/_navbar_public.html` | Barra de navegação da landing page |
| `partials/_messages.html` | Exibição das mensagens do Django (`messages`) |

---

## Regras gerais

- Todo elemento interativo deve ter `transition-all duration-200`
- Nunca usar fundo claro — o sistema é exclusivamente dark mode
- Erros de formulário são sempre exibidos em `text-red-400` abaixo do campo
- Mensagens de sucesso do Django usam estilo `emerald`, erros usam `red`, avisos usam `amber`
- `{% csrf_token %}` obrigatório em todo `<form>` com método POST
