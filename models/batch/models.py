"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************
"""
import uuid

from django.utils import timezone
from django.db import models

from .managers.batch_manager import BatchManager

class Batch(models.Model):
    """
    Batch model
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=250, unique=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)

    objects = BatchManager()

    class Meta:
        """
        model Meta options
        """
        db_table = 'app_batch'

    def __str__(self):
        """
        string representation
        """
        return self.name
