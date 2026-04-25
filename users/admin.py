from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    '''
    Custom UserAdmin to manage the Crivopy User model.
    '''
    
    # 1.7.2 - Configuration of list_display
    list_display = [
        'email', 
        'first_name', 
        'last_name', 
        'is_active', 
        'created_at'
    ]
    
    # Customizing search and ordering for better admin UX
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    # Ensuring the admin uses our custom fields if necessary
    # Note: BaseUserAdmin expects certain fields; since we use email as username, 
    # we override the fieldsets to match our custom User model structure.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    # Making created_at and updated_at read-only as they are auto_now fields
    readonly_fields = ['created_at', 'updated_at']