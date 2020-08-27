"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

auth_user.managers.user_manager
"""
from django.db import models
from django.contrib.auth.models import BaseUserManager

from myproj import logger

LOG = logger.get_logger(__name__)

class UserQueryset(models.query.QuerySet):
    """
    User queryset
    """
    def find_by_email(self, email):
        """
        find by email
        """
        try:
            return self.get(email=email)
        except self.model.DoesNotExist:
            return None

    def find_by_username(self, username):
        """
        find by username
        """
        try:
            return self.get(username=username)
        except self.model.DoesNotExist:
            return None

    def filter_by_active(self):
        """
        filter by active
        """
        return self.filter(is_active=True)

    def filter_by_inactive(self):
        """
        filter by inactive
        """
        return self.filter(is_active=False)

class UserManager(BaseUserManager):
    """
    user manager
    """
    def get_queryset(self):
        """
        get queryset
        """
        return UserQueryset(self.model, using=self._db)

    def find_by_email(self, email):
        """
        find by email
        """
        return self.get_queryset().find_by_email(email)

    def find_by_username(self, username):
        """
        find by username
        """
        return self.get_queryset().find_by_username(username)

    def filter_by_active(self):
        """
        filter by active
        """
        return self.get_queryset().filter_by_active()

    def filter_by_inactive(self):
        """
        filter by inactive
        """
        return self.get_queryset().filter_by_inactive()
