"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API upload related services
"""
import os

# django
from django_filters import rest_framework as filters
from django_filters import CharFilter

# logger
from myproj import logger

# models
from models.upload.models import Upload

# libs
from myproj.libs.services.base import BaseService

# utils
from myproj.utils.handler.exception import InvalidInput, NotFound

# serializers
from ..serializers.upload_serializers import (
    ResumableUploadSerializer, UploadSerializer, PatchUploadSerializer)

LOG = logger.get_logger(__name__)

class UploadService(BaseService):
    """
    upload service
    """
    def run(self):
        """
        run service
        """
        self.serializer = ResumableUploadSerializer
        serializer = self.serializer(data=self.data, context={'request': self.request})
        if not serializer.is_valid():
            LOG.error(serializer.errors)
            self.errors = serializer.errors
            raise InvalidInput
        return serializer.save()


class GetUploadService(BaseService):
    """
    get upload service
    """
    def get_queryset(self):
        """
        get queryset
        """
        instance = Upload.objects.all()
        if self.uuid:
            self.many=False
            instance = instance.find_by_uuid(self.uuid)
            if not instance:
                self.errors = {'instance': 'Invalid instance'}
                raise NotFound
        return instance

    def run(self):
        """
        run service
        """
        self.serializer = UploadSerializer
        serializer = self.serializer(self.get_queryset(), many=self.many)
        self.instance = serializer.instance
        return serializer.data

class PatchUploadService(GetUploadService):
    """
    patch upload service
    """
    def run(self):
        """
        run service
        """
        self.serializer = PatchUploadSerializer
        serializer = self.serializer(self.get_queryset(), data=self.data)
        self.instance = serializer.instance
        if not serializer.is_valid():
            self.errors = serializer.errors
            raise InvalidInput
        serializer.save()
        return UploadSerializer(self.instance).data

class DeleteUploadService(GetUploadService):
    """
    patch upload service
    """
    def delete_file(self, file_location):
        """
        delete file
        """
        try:
            os.unlink(file_location)
        except FileNotFoundError:
            pass

    def run(self):
        """
        run service
        """
        self.instance = self.get_queryset()
        self.delete_file(self.instance.path)
        self.instance.delete()
        return None

class FilterUploadService(filters.FilterSet):
    """
    Filter batch
    """
    id = CharFilter(method='get_by_id')
    file_name = CharFilter(method='get_by_name')
    date_created = CharFilter(method='get_by_created')

    def get_by_id(self, queryset, name, value):
        """
        handler for filter[id]=<pk>
        """
        return queryset.filter_by_id(value)

    def get_by_name(self, queryset, name, value):
        """
        handler for filter[name]=<name>
        """
        LOG.info('searching batch: %s:%s', name, value)
        if len(value) >= 3:
            return queryset.filter_by_name(value)
        LOG.info('value %s is too short returning default queryset.')
        return queryset

    def get_by_created(self, queryset, name, value):
        """
        handler for filter[date_created]=<YYYY-MM-DD>
        """
        LOG.info('searching batch: %s:%s', name, value)
        return queryset.filter_by_date_created(value)
