"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API upload related views
"""
# filters
from rest_framework_json_api import filters
from rest_framework_json_api import django_filters

# drf yasg
from drf_yasg.utils import swagger_auto_schema

# rest framework
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

# libs
from myproj.libs.api.api_response import ApiResponse

# exception
from myproj.utils.handler.exception import NotFound, InvalidInput

# logger
from myproj import logger

# services
from ..services.upload_services import (
    UploadService, GetUploadService, FilterUploadService, PatchUploadService, DeleteUploadService)
from ..services.download_services import DownloadService

# serializers
from ..serializers.upload_serializers import ResumableUploadSerializer, UploadSerializer

from myproj.libs.api.base import BaseAPIView

LOG = logger.get_logger(__name__)

class UploadView(BaseAPIView):
    """
    upload view
    """
    permission_classes = [IsAuthenticated,]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ResumableUploadSerializer
    services_post = UploadService
    services_get = GetUploadService

    filterset_class = FilterUploadService
    filter_backends = (
        filters.QueryParameterValidationFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend
    )

    http_method_names = ['post', 'get',]

    @swagger_auto_schema(tags=['upload',])
    def post(self, request, *args, **kwargs):
        service = UploadService(request=request, data=request.data)
        try:
            resp = service.run()
        except InvalidInput:
            return ApiResponse().unprocessable_entity(data=service.errors)
        except Exception as err:
            LOG.error(err, exc_info=True)
            return ApiResponse().internal_server_error(data={'exception': '%s' % err})

        created = resp.get('created', None)
        if created:
            return ApiResponse().created(data=resp)
        return ApiResponse().success(data=resp)


    @swagger_auto_schema(tags=['upload',])
    def get(self, request, *args, **kwargs):
        self.serializer_class = UploadSerializer
        return super().get(request, *args, **kwargs)

class UploadUUIDView(BaseAPIView):
    """
    upload uuid view
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = UploadSerializer
    services_get = GetUploadService
    services_patch = PatchUploadService
    services_delete = DeleteUploadService

    http_method_names = ['get', 'patch', 'delete']

    @swagger_auto_schema(tags=['upload',])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['upload',])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['upload',])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class DownloadView(BaseAPIView):
    """
    download view
    """
    permission_classes = [IsAuthenticated,]
    services_get = DownloadService

    http_method_names = ['get',]

    @swagger_auto_schema(tags=['upload',])
    def get(self, request, *args, **kwargs):
        try:
            service = self.services_get(request=request, context={}, *args, **kwargs)
            return service.run()
        except NotFound:
            return ApiResponse(request=request).not_found(
                data=service.errors)
        except Exception as err:
            LOG.error('Exception due to: %s', err, exc_info=True)
            return ApiResponse(request=request).internal_server_error(
                data={'exception': '%s' % err})
