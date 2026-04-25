from django.urls import path
from .views import JobAnalysisView, DocumentAnalysisView , AgentChatView, AgentChatClearView


'''
URL configuration for the brain application.
Updated to include RAG analysis trigger.
'''
app_name = 'brain'

urlpatterns = [
    # Task 5.3.2: Analytical dashboard for a specific job
    path(
        'vagas/<int:pk>/analise/', 
        JobAnalysisView.as_view(), 
        name='job-analysis'
    ),
    
    # Task 5B.9.1: Trigger AI RAG analysis for a specific document
    path(
        'documentos/<int:document_pk>/analisar/', 
        DocumentAnalysisView.as_view(), 
        name='document-analyze'
    ),

    # Task 8.7.1: HR Agent chat for a specific job
    path(
        'vagas/<int:job_pk>/agente/',
        AgentChatView.as_view(),
        name='agent-chat'
    ),

    # Task 8.7.2: Clear HR Agent conversation history
    path(
        'vagas/<int:job_pk>/agente/limpar/',
        AgentChatClearView.as_view(),
        name='agent-chat-clear'
    ),

]