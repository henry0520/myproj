"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

tests batch
"""
import json
from django.utils import timezone
from myproj import logger
from myproj.utils import test_base

from models.auth_user.models import User
from models.batch.models import Batch

LOG = logger.get_logger(__name__)

class BatchTests(test_base.UploadMixin, test_base.APITestCase):
    """
    batch test
    """
    def setUp(self):
        """
        custom class setup method
        """
        self.user, _ = User.objects.get_or_create(
            email='test@intervenn.com',
            username='test'
        )

    def post_batch(self, name):
        """
        post batch
        """
        data = {'name': name}
        response = self.client.post(
            '/api/v1/batches/', data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['data']['name'], data['name'])
        return json_response

    def test_post_batch(self):
        """
        test post batch
        """
        self.client.force_authenticate(user=self.user)
        name = 'Test batch'
        json_response = self.post_batch(name)
        self.assertEqual(json_response['data']['name'], name)

    def test_patch_batch(self):
        """
        test patch batch
        """
        self.client.force_authenticate(user=self.user)
        name = 'Test batch'
        json_response = self.post_batch(name)
        self.assertEqual(json_response['data']['name'], name)
        uuid = json_response['data']['uuid']


        data = {'name': 'test batch patch'}
        response = self.client.patch(
            '/api/v1/batches/%s/' % uuid, data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['data']['name'], data['name'])

    def test_delete_batch(self):
        """
        test patch batch
        """
        self.client.force_authenticate(user=self.user)
        name = 'Test batch'
        json_response = self.post_batch(name)
        self.assertEqual(json_response['data']['name'], name)
        uuid = json_response['data']['uuid']

        response = self.client.delete(
             '/api/v1/batches/%s/' % uuid, format='json')
        self.assertEqual(response.status_code, 204)

    def test_filters(self):
        """
        test filter name
        """
        self.client.force_authenticate(user=self.user)

        for x in range(3):
            name = 'batch-%s' % x
            json_response = self.post_batch(name)
            self.assertEqual(json_response['data']['name'], name)

        response = self.client.get(
            '/api/v1/batches/?filter[name]=batch-', format='json')

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        assert(json_response['meta']['count'], 3)


        response = self.client.get(
            '/api/v1/batches/?filter[id]=1', format='json')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        assert(json_response['meta']['count'], 1)


        response = self.client.get(
            '/api/v1/batches/?filter[date_created]=%s' % timezone.now().strftime(
                '%Y-%m-%d'), format='json')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        assert(json_response['meta']['count'], 2)

    def test_unprocessable_entity(self):
        """
        test unprocessable entity 422
        """
        self.client.force_authenticate(user=self.user)
        data = {}
        response = self.client.post(
            '/api/v1/batches/', data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 422)
        json_response = response.json()
        LOG.info(json_response)


    def test_unauthorized(self):
        """
        test unauthorized
        """
        data = {'name': 'not valid'}
        response = self.client.post(
            '/api/v1/batches/', data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        json_response = response.json()
        LOG.info(json_response)
