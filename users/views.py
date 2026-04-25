from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm

class LandingPageView(TemplateView):
    '''
    Renders the public landing page.
    '''
    template_name = 'public/landing.html'

    def dispatch(self, request, *args, **kwargs):
        # Se o usuário já está logado e tenta ver a Landing Page, 
        # mandamos ele direto para o dashboard.
        if request.user.is_authenticated:
            return redirect('hub:dashboard')
        return super().dispatch(request, *args, **kwargs)

class RegisterView(FormView):
    '''
    Handles user registration using RegisterForm.
    '''
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('hub:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Conta criada com sucesso! Por favor, faça o login.')
        return super().form_valid(form)

class LoginView(FormView):
    '''
    Handles user authentication using LoginForm.
    '''
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('hub:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('hub:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        
        user = authenticate(self.request, email=email, password=password)
        
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'E-mail ou senha incorretos.')
            return self.form_invalid(form)

class LogoutView(View):
    '''
    Handles user logout via POST method.
    '''
    def post(self, request):
        logout(request)
        return redirect('landing')