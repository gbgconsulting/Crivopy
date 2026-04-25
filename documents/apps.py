from django.apps import AppConfig

class DocumentsConfig(AppConfig):
    '''
    Configuration for Documents app.
    Ensures signals are connected on startup.
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'documents'
    verbose_name = 'Gestão de Documentos'

    def ready(self):
        '''
        Task 5B.7.2: Connect signals during app initialization.
        '''
        import documents.signals