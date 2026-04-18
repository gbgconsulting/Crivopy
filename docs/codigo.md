# Convenções de Código

---

## Regras gerais

- Linguagem do código: **inglês** (nomes de variáveis, funções, classes, comentários)
- Linguagem da interface: **português brasileiro** (labels, mensagens, textos exibidos ao usuário)
- Estilo: **PEP 8**
- Aspas: **simples** sempre que possível
- Sem over-engineering: preferir soluções nativas do Django antes de adicionar dependências

---

## Exemplo de estilo correto

```python
# Correto
class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'hub/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)
```

```python
# Errado — aspas duplas, sem filtro por usuário
class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "hub/job_list.html"

    def get_queryset(self):
        return Job.objects.all()
```

---

## Views

- Usar **Class-Based Views** (CBV) sempre que possível
- Herdar de `LoginRequiredMixin` em todas as views da área autenticada — sempre como **primeiro** na herança
- Sobrescrever `get_queryset` para filtrar por `request.user`, nunca confiar apenas no `pk` da URL
- Usar `messages.success` e `messages.error` para feedback ao usuário após ações POST

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Job
from .forms import JobForm


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'hub/job_form.html'
    success_url = reverse_lazy('job-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Vaga criada com sucesso.')
        return super().form_valid(form)
```

---

## Models

- Todos os models herdam de `models.Model`
- Todo model deve ter `created_at` e `updated_at`:

```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

- Definir `__str__` em todo model
- Definir `class Meta` com `ordering` quando relevante
- Usar `TextChoices` ou constantes de classe para campos com choices:

```python
class Job(models.Model):
    ACTIVE = 'active'
    PAUSED = 'paused'
    ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (ACTIVE, 'Ativa'),
        (PAUSED, 'Pausada'),
        (ARCHIVED, 'Arquivada'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )
```

---

## Forms

- Usar `ModelForm` sempre que o form mapear diretamente para um model
- Aplicar classes CSS do design system diretamente nos widgets via `attrs`:

```python
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-gray-800 border border-gray-700 '
                         'text-gray-100 placeholder-gray-500 focus:outline-none '
                         'focus:ring-2 focus:ring-indigo-500 focus:border-transparent '
                         'transition-all duration-200',
                'placeholder': 'Título da vaga',
            }),
        }
```

---

## Signals

- Signals ficam em `<app>/signals.py`
- Conectados no método `ready()` de `<app>/apps.py`:

```python
# documents/apps.py
class DocumentsConfig(AppConfig):
    name = 'documents'

    def ready(self):
        import documents.signals  # noqa: F401
```

```python
# documents/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Document


@receiver(post_delete, sender=Document)
def delete_document_file(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
```

---

## Segurança

- `{% csrf_token %}` obrigatório em todo `<form>` com método POST nos templates
- Views que operam sobre objetos (update, delete) devem filtrar por `request.user` via `get_queryset`, nunca apenas pelo `pk`
- Uploads: validar extensão (`.pdf`) e tipo MIME (`application/pdf`) no `clean()` do form
- Arquivos enviados são salvos em `MEDIA_ROOT` e servidos via `/media/` apenas em desenvolvimento

---

## URLs

- Nomes de rotas em **kebab-case**: `job-list`, `document-upload`, `job-analysis`
- Usar `reverse_lazy()` nas views e `{% url %}` nos templates
- Nunca escrever URLs hardcoded no código

---

## Templates

- Todos herdam de `base.html` ou `base_authenticated.html`
- Variáveis de contexto em **snake_case**: `job_list`, `document`, `analysis`
- Mensagens do Django exibidas via `{% include 'partials/_messages.html' %}`
- Texto exibido ao usuário sempre em **português brasileiro**
