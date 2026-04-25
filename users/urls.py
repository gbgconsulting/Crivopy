from django.urls import path
from .views import (
    LandingPageView,
    RegisterView,
    LoginView,
    LogoutView
)

urlpatterns = [
    # 1.5.2 - Public landing page
    path('', LandingPageView.as_view(), name='landing'),

    # 1.5.3 - User registration route
    path('cadastro/', RegisterView.as_view(), name='register'),

    # 1.5.4 - User login route
    path('entrar/', LoginView.as_view(), name='login'),

    # 1.5.5 - User logout route
    path('sair/', LogoutView.as_view(), name='logout'),
]