from django import forms
from django.core.exceptions import ValidationError
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    '''
    Form for uploading candidate resumes.
    Includes strict PDF validation and TailwindCSS styling.
    '''
    class Meta:
        model = Document
        fields = ['candidate_name', 'candidate_email', 'file', 'notes']
        widgets = {
            'candidate_name': forms.TextInput(attrs={
                'class': 'w-full bg-[#111114] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200',
                'placeholder': 'Nome completo do candidato'
            }),
            'candidate_email': forms.EmailInput(attrs={
                'class': 'w-full bg-[#111114] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200',
                'placeholder': 'exemplo@email.com'
            }),
            'file': forms.FileInput(attrs={
                'class': 'w-full bg-[#111114] border border-white/10 rounded-xl px-4 py-3 text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-700 transition-all cursor-pointer',
                'accept': '.pdf'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full bg-[#111114] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200',
                'placeholder': 'Observações adicionais sobre o candidato...',
                'rows': 3
            }),
        }
        labels = {
            'candidate_name': 'Nome do Candidato',
            'candidate_email': 'E-mail de Contato',
            'file': 'Currículo (PDF)',
            'notes': 'Notas Internas',
        }

    def clean_file(self):
        '''
        Task 4.3.3: Strict validation for PDF extension and MIME type.
        '''
        file = self.cleaned_data.get('file')
        
        if file:
            # 1. Check file extension
            if not file.name.lower().endswith('.pdf'):
                raise ValidationError('O arquivo deve estar no formato PDF.')
            
            # 2. Check MIME type (Content Type)
            if file.content_type != 'application/pdf':
                raise ValidationError('O tipo do arquivo deve ser application/pdf.')
            
        return file

class DocumentStatusForm(forms.ModelForm):
    '''
    Task 4.3.5: Simplified form for updating document status only.
    '''
    class Meta:
        model = Document
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full bg-[#111114] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200'
            }),
        }
        labels = {
            'status': 'Alterar Status para',
        }