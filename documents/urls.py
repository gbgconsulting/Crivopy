from django.urls import path
from . import views

'''
URL configuration for the documents application.
Handles candidate resume management and status updates.
'''

urlpatterns = [
    # Task 4.5.2: List documents for a specific job
    path(
        'vagas/<int:job_pk>/documentos/', 
        views.DocumentListView.as_view(), 
        name='document-list'
    ),
    
    # Task 4.5.3: Upload a new resume for a specific job
    path(
        'vagas/<int:job_pk>/documentos/upload/', 
        views.DocumentUploadView.as_view(), 
        name='document-upload'
    ),
    
    # Task 4.5.4: Update the status of a specific document
    path(
        'documentos/<int:pk>/status/', 
        views.DocumentStatusUpdateView.as_view(), 
        name='document-status'
    ),
    
    # Task 4.5.5: Delete a document record
    path(
        'documentos/<int:pk>/excluir/', 
        views.DocumentDeleteView.as_view(), 
        name='document-delete'
    ),
]