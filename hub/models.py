from django.db import models
from django.conf import settings

class Job(models.Model):
    '''
    Represents a job position created by a recruiter.
    Central model for managing candidates and documents.
    '''
    
    # Status constants (Portuguese labels for UI)
    ACTIVE = 'ACTIVE'
    PAUSED = 'PAUSED'
    ARCHIVED = 'ARCHIVED'

    STATUS_CHOICES = [
        (ACTIVE, 'Ativa'),
        (PAUSED, 'Pausada'),
        (ARCHIVED, 'Arquivada'),
    ]

    # Task 3.1.2: FK to User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    # Task 3.1.3: Title
    title = models.CharField(max_length=255)

    # Task 3.1.4: Description
    description = models.TextField(blank=True)

    # Task 3.1.5: Status with choices
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE
    )

    # Task 3.1.6: Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Task 3.1.8: Meta configuration
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'

    # Task 3.1.7: String representation
    def __str__(self):
        return self.title