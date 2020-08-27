"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API views.batch_views
"""
# filters
from rest_framework_json_api import filters
from rest_framework_json_api import django_filters

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# rest framework
from rest_framework.permissions import IsAuthenticated

# services
from ..services.batch_services import (
    BatchService, GetBatchService, FilterBatchService, BatchUUIDService, PatchBatchService,
    DeleteBatchService)

# serializers
from ..serializers.batch_serializers import BatchSerializer, BatchUploadSerializer

from myproj.libs.api.base import BaseAPIView

class BatchView(BaseAPIView):
    """
    Batch View
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = BatchSerializer
    services_post = BatchService
    services_get = GetBatchService

    filterset_class = FilterBatchService
    filter_backends = (
        filters.QueryParameterValidationFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend
    )

    http_method_names = ['post', 'get',]

    @swagger_auto_schema(tags=['batch'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(tags=['batch'])
    def get(self, request, *args, **kwargs):
        self.serializer_class = BatchUploadSerializer
        return super().get(request, *args, **kwargs)


class BatchUUIDView(BaseAPIView):
    """
    Batch UUID View
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = BatchSerializer
    services_get = BatchUUIDService
    services_patch = PatchBatchService
    services_delete = DeleteBatchService

    http_method_names = ['get', 'patch', 'delete',]

    @swagger_auto_schema(tags=['batch'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['batch'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['batch'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

