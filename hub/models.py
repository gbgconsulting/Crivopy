from django.db import models
from django.conf import settings
from core.models import TimestampedModel

class Job(TimestampedModel):
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('paused', 'Pausada'),
        ('archived', 'Arquivada'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
