from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm

class LandingPageView(TemplateView):
    template_name = 'public/landing.html'

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Conta criada com sucesso! Faça login para continuar.')
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, 'E-mail ou senha inválidos.')
            return self.form_invalid(form)

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('landing')
    
    def get(self, request):
        return redirect('landing')
