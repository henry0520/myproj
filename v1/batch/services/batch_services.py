"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API batch related services
"""
# django
from django_filters import rest_framework as filters
from django_filters import CharFilter

# logger
from myproj import logger

# models
from models.batch.models import Batch

# libs
from myproj.libs.services.base import BaseService

# utils
from myproj.utils.handler.exception import InvalidInput, NotFound

# serializers
from ..serializers.batch_serializers import BatchSerializer, BatchUploadSerializer

LOG = logger.get_logger(__name__)

class BatchService(BaseService):
    """
    batch service
    """
    def run(self):
        """
        run service
        """
        self.serializer = BatchSerializer
        serializer = self.serializer(data=self.data)
        if not serializer.is_valid():
            self.errors = serializer.errors
            raise InvalidInput
        serializer.save()
        return serializer.data

class GetBatchService(BaseService):
    """
    batch get service
    """
    def get_queryset(self):
        """
        get queryset
        """
        instance = Batch.objects.all()
        if self.uuid:
            self.many = False
            instance = instance.find_by_uuid(self.uuid)
            if not instance:
                self.errors = {'instance': 'Invalid instance'}
                raise NotFound
        return instance

    def run(self):
        """
        run service
        """
        self.serializer = BatchSerializer
        serializer = self.serializer(self.get_queryset(), many=self.many)
        self.instance = serializer.instance
        return BatchUploadSerializer(self.instance, many=self.many).data

class BatchUUIDService(GetBatchService):
    """
    batch uuid service
    """
    def run(self):
        """
        Run service
        """
        self.serializer = BatchSerializer
        serializer = self.serializer(self.get_queryset(), many=self.many)
        self.instance = serializer.instance
        return BatchUploadSerializer(self.instance, many=self.many).data

class PatchBatchService(GetBatchService):
    """
    patch batch service
    """
    def run(self):
        """
        run service
        """
        self.serializer = BatchSerializer
        serializer = self.serializer(self.get_queryset(), data=self.data)
        if not serializer.is_valid():
            self.errors = serializer.errors
            raise InvalidInput
        serializer.save()
        return BatchUploadSerializer(serializer.instance).data

class DeleteBatchService(GetBatchService):
    """
    delete batch service
    """
    def run(self):
        """
        run service
        """
        self.instance = self.get_queryset()
        self.instance.delete()
        return None


class FilterBatchService(filters.FilterSet):
    """
    Filter batch
    """
    id = CharFilter(method='get_by_id')
    name = CharFilter(method='get_by_name')
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
