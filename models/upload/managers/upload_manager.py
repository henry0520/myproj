"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

auth_user.managers.user_manager
"""
from dateparser import parse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError

from myproj import logger

from models.batch.managers.batch_manager import UserQueryset

LOG = logger.get_logger(__name__)

class UploadQueryset(UserQueryset):
    """
    upload queryset
    """

class UploadManager(BaseUserManager):
    """
    upload manager
    """
    def get_queryset(self):
        """
        get queryset
        """
        return UploadQueryset(self.model, using=self._db)

    def find_by_uuid(self, uuid):
        """
        find by uuid
        """
        return self.get_queryset().find_by_uuid(uuid)

    def find_by_name(self, name):
        """
        find by username
        """
        return self.get_queryset().find_by_name(name)

    def exclude_by_uuid(self, uuid):
        """
        exclude by uuid
        """
        return self.get_queryset().exclude_by_uuid(uuid)

    def filter_by_id(self, id):
        """
        filter by id
        """
        return self.get_queryset().filter_by_id(id)

    def filter_by_name(self, name):
        """
        filter by name
        """
        return self.get_queryset().filter_by_name(name)

    def filter_by_date_created(self, date):
        """
        filter by date
        """
        return self.get_queryset().filter_by_date_created(name)
