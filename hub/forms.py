from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-gray-800 border border-gray-700 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Título da vaga'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-gray-800 border border-gray-700 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none transition-all duration-200',
                'placeholder': 'Requisitos e descrição...',
                'rows': 5
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl bg-gray-800 border border-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200'
            }),
        }
