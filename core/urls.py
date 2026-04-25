from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    # App Users: Landing page, Login, Register (na raiz '')
    path('', include('users.urls')),

    # App Hub: Dashboard e Vagas (com prefixo 'hub/')
    path('hub/', include('hub.urls', namespace='hub')),

    # Demais Apps
    path('documents/', include('documents.urls')),
    path('brain/', include('brain.urls')),
    path('chat/', include('chat.urls')),
]

# 0.4.3 - Servir arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)