from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    '''
    Admin configuration for Job model.
    Provides easy management and filtering of job positions.
    '''
    
    # Task 3.6.2: Columns to display in the list view
    list_display = [
        'title', 
        'user', 
        'status', 
        'created_at'
    ]
    
    # Task 3.6.3: Filters and search capabilities
    list_filter = [
        'status', 
        'created_at',
        'user'
    ]
    
    search_fields = [
        'title', 
        'description'
    ]
    
    # UI Refinements
    list_editable = ['status']
    raw_id_fields = ['user']
    ordering = ['-created_at']
    
    # Task 3.6.1: Model is registered via the decorator @admin.register(Job)