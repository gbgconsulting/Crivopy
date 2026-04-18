from django.db import models
from core.models import TimestampedModel

class Document(TimestampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('reviewing', 'Em análise'),
        ('approved', 'Aprovado'),
        ('rejected', 'Reprovado'),
    ]

    job = models.ForeignKey(
        'hub.Job',
        on_delete=models.CASCADE,
        related_name='documents'
    )
    candidate_name = models.CharField(max_length=255)
    candidate_email = models.EmailField(blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.candidate_name} - {self.job.title}'
