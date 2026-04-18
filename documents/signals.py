import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Document

@receiver(post_delete, sender=Document)
def delete_file_on_document_delete(sender, instance, **kwargs):
    '''
    Deletes the physical file from the server when the Document record is deleted.
    '''
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
