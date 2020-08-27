"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

tests upload
"""
import os
import json

from myproj import logger
from myproj.utils import test_base

from models.auth_user.models import User

LOG = logger.get_logger(__name__)

class LoginTests(test_base.APITestCase):
    """
    login test
    """

    def setUp(self):
        """
        custom class setup method
        """
        self.user, _ = User.objects.get_or_create(
            email='test@intervenn.com',
            username='test'
        )

        self.user.set_password('Test1234!')
        self.user.save()

    def test_login(self):
        """
        test login
        """
        data = {'email': self.user.email, 'password': 'Test1234!'}
        response = self.client.post(
            '/api/v1/accounts/login/', data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        LOG.info(json_response)
