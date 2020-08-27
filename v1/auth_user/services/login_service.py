"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API myproj.libs.services.base
"""
# rest_framework
from rest_framework.authtoken.models import Token

# models
from models.auth_user.models import User

# libs
from myproj.libs.services.base import BaseService

# utils
from myproj.utils.handler.exception import Unauthorized, InvalidInput

# serializers
from ..serializers.login_serializer import LoginSerializer

from myproj import logger
LOG = logger.get_logger(__name__)

class LoginService(BaseService):
    """
    Login login service
    """
    @staticmethod
    def get_or_create_token(user):
        """
        Get or create token
        """
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def invalid_credential(self):
        """
        Invalid credential
        """
        self.errors = {'credential': 'Invalid username or password.'}
        raise Unauthorized

    def run(self):
        """
        Run service
        """
        self.serializer = LoginSerializer

        # Validate email and password
        active_user = User.objects.filter_by_active()

        # Query by email
        user = active_user.find_by_email(email=self.data.get('email'))

        # Raise error if user does not exist
        if not user:
            self.invalid_credential()

        is_authenticated = self.backend_authentication(user)
        if is_authenticated is False:
            self.invalid_credential()

        serializer = self.serializer(data=self.data)
        if not serializer.is_valid():
            self.errors = serializer.errors
            raise InvalidInput

        return {'token': self.get_or_create_token(user)}

    def backend_authentication(self, user):
        """
        backend authentication
        """
        if user.check_password(self.data['password']) is False:
            return False
        return True
