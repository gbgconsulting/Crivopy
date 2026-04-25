from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    '''
    Form for creating and updating Job instances.
    Includes TailwindCSS classes for a consistent dark-themed UI.
    '''
    class Meta:
        model = Job
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-[#111114] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200 placeholder:text-gray-500',
                'placeholder': 'Ex: Desenvolvedor Python Sênior'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-[#111114] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200 placeholder:text-gray-500',
                'placeholder': 'Descreva as responsabilidades e requisitos da vaga...',
                'rows': 5
            }),
            'status': forms.Select(attrs={
                'class': 'w-full bg-[#111114] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200'
            }),
        }
        labels = {
            'title': 'Título da Vaga',
            'description': 'Descrição',
            'status': 'Status Inicial',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure that even if classes are changed, basic styling remains consistent
        for field_name, field in self.fields.items():
            if field_name == 'status':
                field.empty_label = None # Remove '---------' from select