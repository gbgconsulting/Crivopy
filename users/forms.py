from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Centralized CSS Classes for the Design System (Ref: 1.3.6)
INPUT_CLASSES = 'w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all placeholder:text-gray-600'

class RegisterForm(forms.ModelForm):
    '''
    Form for user registration with password confirmation and styling.
    '''
    password = forms.CharField(
        label=_('Senha'),
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'placeholder': '••••••••'})
    )
    password_confirm = forms.CharField(
        label=_('Confirmar Senha'),
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'placeholder': '••••••••'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': _('Nome'),
            'last_name': _('Sobrenome'),
            'email': _('E-mail'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Seu nome'}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Seu sobrenome'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'exemplo@crivopy.com'}),
        }

    def clean_password_confirm(self):
        '''
        1.3.3: Validation to check if passwords match.
        '''
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(_('As senhas não conferem.'))
        return password_confirm

    def save(self, commit=True):
        '''
        1.3.4: Save the user with a secure password hash.
        '''
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    '''
    1.3.5: Standard login form with email and password fields.
    '''
    email = forms.EmailField(
        label=_('E-mail'),
        widget=forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'seu@email.com'})
    )
    password = forms.CharField(
        label=_('Senha'),
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'placeholder': '••••••••'})
    )