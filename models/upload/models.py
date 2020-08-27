"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************
"""
import uuid
import errno
import os
import mimetypes
from slugify import slugify as slugify_unicode
from jsonfield import JSONField
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.files import File
from django.urls import reverse

from myproj.libs import crypto

from models.auth_user.models import User
from models.batch.models import Batch

from .managers.upload_manager import UploadManager

class Upload(models.Model):
    """
    Upload
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, db_index=True, null=True, on_delete=models.deletion.SET_NULL)
    batch = models.ForeignKey(
        Batch, related_name='uploads', db_index=True, null=True, on_delete=models.deletion.SET_NULL)
    file_id = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    valid = models.BooleanField(default=False)
    content_type = models.CharField(max_length=250, blank=True, null=True)
    path = models.CharField(max_length=255, db_index=True)
    date_created = models.DateTimeField(default=timezone.now, db_index=True)
    uploaded_chunks = JSONField(default=dict)
    uploaded_size = models.BigIntegerField(null=True)

    objects = UploadManager()

    class Meta:
        """
        meta option
        """
        unique_together = ['user', 'batch', 'file_id']
        ordering = ['-date_created']
        db_table = 'app_upload'

    def __init__(self, *args, **kwargs):
        """
        initialization
        """
        super().__init__(*args, **kwargs)
        if not self.path:
            self.path = self.generate_upload_path()

    @property
    def c_type(self):
        """
        return the content-type based on filename
        """
        content_type = mimetypes.guess_type(self.name)[0]
        return content_type or 'application/octet-stream'

    def open(self):
        """
        open file as read-write in binary
        """
        try:
            return File(open(self.path, 'r+b'))
        except IOError as err:
            if err.errno == errno.ENOENT:
                os.open(self.path, os.O_CREAT)
                return File(open(self.path, 'r+b'))
            raise

    @staticmethod
    def generate_upload_path():
        """
        generate upload path where the file with be stored
        """
        return '{0}{1}.upload'.format(settings.UPLOAD_DIR, crypto.random_alnum(32))

    def retrieve(self):
        """
        retrieve
        returns a yielded chuncks
        """
        plain = File(open(self.path, 'rb'))
        return plain.chunks(settings.RETRIEVE_CHUNK_SIZE)

    @property
    def download_link(self):
        """
        return the reverse url of uploaded file
        """
        return reverse(
            'uploaded-download',
            kwargs={'uuid': self.uuid}
        )

    @property
    def download_filename(self):
        """
        download filename
        """
        ext = mimetypes.guess_extension(self.content_type)
        filename = '.'.join([self.name, ext])
        return slugify_unicode(filename, ok=settings.VALID_LABEL_CHARACTERS)

    def update_chunks_data(self, data):
        """
        track how many chucks where uploaded
        """
        self.uploaded_chunks[data['chunk_number']] = data
        self.uploaded_size = data['uploaded_size']
        self.save()
