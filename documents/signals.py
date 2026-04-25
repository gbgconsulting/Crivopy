import os
import logging
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Document
from brain.vector_store import delete_document_chunks

# Configure logger for traceability
logger = logging.getLogger(__name__)

@receiver(post_delete, sender=Document)
def handle_document_cleanup(sender, instance, **kwargs):
    '''
    Task 5B.7.1: Signal to clean up physical files and vector chunks 
    whenever a Document is deleted.
    '''
    
    # 1. Physical File Cleanup (Maintain logic from Task 4.2)
    if instance.file:
        if os.path.isfile(instance.file.path):
            try:
                os.remove(instance.file.path)
                logger.info(f'Physical file removed: {instance.file.path}')
            except Exception as e:
                logger.error(f'Failed to delete file {instance.file.path}: {e}')

    # 2. Vector Store Cleanup (Task 5B.7.1 implementation)
    try:
        # We call the service that interacts with ChromaDB
        delete_document_chunks(document_id=instance.id)
        logger.info(f'Vector chunks removed from ChromaDB for Document ID: {instance.id}')
    except Exception as e:
        # We log the error but allow the DB transaction to complete
        logger.error(f'Failed to delete vector chunks for Document {instance.id}: {e}')