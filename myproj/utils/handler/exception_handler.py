# core
from rest_framework.views import exception_handler
from rest_framework.routers import APIRootView

from django.conf import settings
from django.utils.module_loading import import_string
from django.template.loader import render_to_string

from myproj import logger

# libs
from ...libs.api.api_response import ApiResponse

# logger
LOG = logger.get_logger(__name__)


def custom_handler(exc, context):
    """
    custom exeption hanlder
    """
    LOG.info("Executing custom_handler..")
    request = context.get('request')
    view = context.get('view', None)
    response = exception_handler(exc, context)

    if response is not None:
        code = exc.get_full_details().get('code')
        data = {'%s' % code : response.data['detail']}
        api_response = ApiResponse()
        api_response.set_status(response.status_code)
        response_data = api_response.get_error_data(
            message=code, data=data)
        LOG.info("custom_handler --> Returning API response")
        return api_response.api_response(response_data)
    LOG.info("custom_handler --> Returning regular response")
    return response


def error404(request, exception):
    """
    custom 404 error handler
    """
    return ApiResponse(request=request).not_found(
        data={'not_found': 'Invalid page.'})


def error500(request):
    """
    custom 500 error handler
    """
    return ApiResponse(request=request).internal_server_error(
        data={'exception': 'Something went wrong'})
