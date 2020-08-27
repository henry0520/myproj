"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API views.auth_user
"""
from drf_yasg.utils import swagger_auto_schema
from ..serializers.login_serializer import LoginSerializer
from ..services.login_service import LoginService
from myproj.libs.api.base import BaseAPIView

class LoginView(BaseAPIView):
    """
    Login View
    """
    permission_classes = []
    serializer_class = LoginSerializer
    services_post = LoginService

    http_method_names = ['post', 'options']

    @swagger_auto_schema(tags=['accounts'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(tags=['accounts'])
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
