from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from core import settings

class Analysis(models.Model):
    '''
    Represents the AI-generated analysis of a candidate's document.
    Updated to support RAG pipeline status tracking.
    '''

    # Task 5B.5.2: RAG Status Choices
    PENDING = 'pending'
    PROCESSING = 'processing'
    DONE = 'done'
    ERROR = 'error'

    RAG_STATUS_CHOICES = [
        (PENDING, 'Pendente'),
        (PROCESSING, 'Processando'),
        (DONE, 'Concluído'),
        (ERROR, 'Erro'),
    ]

    # Existing Fields (Task 5B.5.1 Confirmation)
    job = models.ForeignKey(
        'hub.Job', 
        on_delete=models.CASCADE, 
        related_name='analyses'
    )
    document = models.ForeignKey(
        'documents.Document', 
        on_delete=models.CASCADE, 
        related_name='analyses'
    )
    summary = models.TextField(blank=True)
    score = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Task 5B.5.2: Field to track the pipeline state
    rag_status = models.CharField(
        max_length=20,
        choices=RAG_STATUS_CHOICES,
        default=PENDING
    )

    # Task 5B.5.3: Field for technical error details
    error_message = models.TextField(blank=True)

    # Timestamps (Task 5B.5.1 Confirmation)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Análise'
        verbose_name_plural = 'Análises'
        ordering = ['-created_at']
        unique_together = ('job', 'document')

    def __str__(self):
        return f'Analysis {self.id}: {self.document.candidate_name} ({self.rag_status})'


class DocumentChunk(models.Model):
    '''
    Task 5B.6.1: Stores individual pieces of text from a document.
    Links the relational database with the ChromaDB vector IDs.
    '''
    
    # Relationship to the original document
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.CASCADE,
        related_name='chunks'
    )
    
    # The order of the chunk in the original document
    chunk_index = models.IntegerField()
    
    # The actual text content of the chunk
    content = models.TextField()
    
    # Reference to the ID used within ChromaDB
    embedding_id = models.CharField(max_length=255)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pedaço de Documento'
        verbose_name_plural = 'Pedaços de Documentos'
        ordering = ['document', 'chunk_index']
        # Ensures index order is unique per document
        unique_together = ('document', 'chunk_index')

    def __str__(self):
        return f'Chunk {self.chunk_index} of {self.document.candidate_name}'
    
def __str__(self):
        return f'Chunk {self.chunk_index} of {self.document.candidate_name}'


class AgentConversation(models.Model):  # ← sem indentação, fora do DocumentChunk
    job = models.ForeignKey(
        'hub.Job',
        on_delete=models.CASCADE,
        related_name='agent_conversations',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    messages = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Conversa: {self.job.title} ({self.user.email})'