from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    '''
    Admin configuration for Document model.
    Facilitates the management of candidate resumes and their processing status.
    '''
    
    # Task 4.7.2: Columns to display in the list view
    list_display = [
        'candidate_name', 
        'job', 
        'status', 
        'created_at'
    ]
    
    # Task 4.7.2: Filters to segment data
    list_filter = [
        'status', 
        'job__user', # Filters by recruiter who owns the job
        'created_at'
    ]
    
    # Task 4.7.2: Search functionality
    search_fields = [
        'candidate_name', 
        'candidate_email',
        'job__title'
    ]
    
    # Technical refinements for the admin interface
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['job', 'job__user'] # Optimization to reduce DB queries
    raw_id_fields = ['job'] # Better UI for selecting jobs in large databases
    
    # Task 4.7.1: Model is registered via the decorator @admin.register(Document)