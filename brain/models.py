from django.db import models
from core.models import TimestampedModel

class Analysis(TimestampedModel):
    RAG_STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('done', 'Concluído'),
        ('error', 'Erro'),
    ]

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
    score = models.IntegerField(null=True, blank=True)
    rag_status = models.CharField(
        max_length=20,
        choices=RAG_STATUS_CHOICES,
        default='pending'
    )
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f'Análise: {self.document.candidate_name} - {self.job.title}'

class DocumentChunk(TimestampedModel):
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.CASCADE,
        related_name='chunks'
    )
    chunk_index = models.IntegerField()
    content = models.TextField()
    embedding_id = models.CharField(max_length=255)

    def __str__(self):
        return f'Chunk {self.chunk_index} - {self.document.candidate_name}'
