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

LOG = logger.get_logger(__name__)

class UserQueryset(models.query.QuerySet):
    """
    User queryset
    """
    def find_by_uuid(self, uuid):
        """
        find by username
        """
        try:
            return self.get(uuid=uuid)
        except (self.model.DoesNotExist, ValidationError):
            return None

    def find_by_name(self, name):
        """
        find by username
        """
        try:
            return self.get(name=name)
        except self.model.DoesNotExist:
            return None

    def exclude_by_uuid(self, uuid):
        """
        Exclude by uuid
        """
        try:
            return self.exclude(uuid=uuid)
        except ValidationError:
            return self.filter().none()

    def filter_by_id(self, id):
        """
        filter by id
        """
        return self.filter(id=id)

    def filter_by_name(self, name):
        """
        Filter by name
        """
        return self.filter(name__icontains=name)

    def filter_by_date_created(self, date):
        """
        filter by date created
        """
        start_date = parse(str(date))
        if start_date:
            end_date = timezone.make_aware(
                timezone.datetime.combine(
                    start_date.date(),
                    start_date.time().max
                )
            )
            return self.filter(date_created__gte=start_date, date_created__lte=end_date)
        return self.filter.none()

class BatchManager(BaseUserManager):
    """
    user manager
    """
    def get_queryset(self):
        """
        get queryset
        """
        return UserQueryset(self.model, using=self._db)

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
