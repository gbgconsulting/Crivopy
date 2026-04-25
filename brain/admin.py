from django.contrib import admin
from .models import Analysis

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    '''
    Admin configuration for the Analysis model.
    Provides visibility into AI processing results and scores.
    '''
    
    # Task 5.5.1: Model registration and display configuration
    list_display = [
        'get_candidate_name', 
        'get_job_title', 
        'score', 
        'created_at'
    ]
    
    list_filter = [
        'score', 
        'job', 
        'created_at'
    ]
    
    search_fields = [
        'document__candidate_name', 
        'job__title', 
        'summary'
    ]
    
    # Technical optimizations
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['job', 'document'] # Prevents N+1 query issues
    
    # Custom display methods for better readability
    @admin.display(ordering='document__candidate_name', description='Candidato')
    def get_candidate_name(self, obj):
        return obj.document.candidate_name

    @admin.display(ordering='job__title', description='Vaga')
    def get_job_title(self, obj):
        return obj.job.title