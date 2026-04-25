from django.db import models

class Document(models.Model):
    '''
    Represents a candidate document (resume/CV) uploaded for a specific job.
    This model stores file references and status for the RAG pipeline.
    '''

    # Task 4.1.6: Status Constants
    PENDING = 'PENDING'
    REVIEWING = 'REVIEWING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

    STATUS_CHOICES = [
        (PENDING, 'Pendente'),
        (REVIEWING, 'Em Revisão'),
        (APPROVED, 'Aprovado'),
        (REJECTED, 'Reprovado'),
    ]

    # Task 4.1.2: FK to Job (from hub app)
    job = models.ForeignKey(
        'hub.Job',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    # Task 4.1.3: Candidate Name
    candidate_name = models.CharField(max_length=255)

    # Task 4.1.4: Candidate Email
    candidate_email = models.EmailField(blank=True)

    # Task 4.1.5: PDF File storage
    file = models.FileField(upload_to='documents/%Y/%m/')

    # Task 4.1.6: Status field
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    # Task 4.1.7: Additional notes
    notes = models.TextField(blank=True)

    # Task 4.1.8: Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Task 4.1.10: Meta configuration
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    # Task 4.1.9: String representation
    def __str__(self):
        return self.candidate_name