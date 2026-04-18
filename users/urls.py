from django.urls import path
from .views import LandingPageView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('cadastro/', RegisterView.as_view(), name='register'),
    path('entrar/', LoginView.as_view(), name='login'),
    path('sair/', LogoutView.as_view(), name='logout'),
]
