"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

tests upload
"""
import os
import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.core import mail

from myproj import logger
from myproj.utils import test_base

from models.auth_user.models import User
from models.upload.models import Upload

LOG = logger.get_logger(__name__)

@override_settings(UPLOAD_DIR='/tmp/test/upload/')
class ResumableUploadTests(test_base.UploadMixin, test_base.APITestCase):
    """
    Base class for Resumable upload test cases
    """
    def setUp(self):
        """
        custom class setup method
        """
        os.makedirs('/tmp/test/upload', exist_ok=True)
        self.user, _ = User.objects.get_or_create(
            email='test@intervenn.com',
            username='test'
        )
        self.user.set_password('Test1234!')
        self.user.save()
        token = '{0} {1}'.format('Token', self.get_token())
        self.client.credentials(HTTP_AUTHORIZATION=token)

        name = 'Test batch - 1'
        json_response = self.create_batch(name)
        batch_id = json_response['data']['uuid']

        file_name='test_file_upload_1'
        self.upload_a_file(file_name, batch_id, size_in_mb=10)


        name = 'Test batch - 2'
        json_response = self.create_batch(name)
        batch_id = json_response['data']['uuid']

        file_name='test_file_upload_2'
        self.upload_a_file(file_name, batch_id, size_in_mb=11)


        name = 'Test batch - 3'
        json_response = self.create_batch(name)
        batch_id = json_response['data']['uuid']

        file_name='test_file_upload_3'
        self.upload_a_file(file_name, batch_id, size_in_mb=12)


    def get_token(self):
        """
        get token
        """
        data = {'email': self.user.email, 'password': 'Test1234!'}
        response = self.client.post(
            '/api/v1/accounts/login/', data=json.dumps(data),
            content_type="application/json")
        json_response = response.json()
        token = json_response['data']['token']
        return token

    def upload_a_file(self, name='test_file_upload', batch_id=None, size_in_mb=10):
        """
        upload a file
        """
        chunk_size = 1024000
        file = self.create_test_file(name, size_in_mb=10)
        file_obj = open(file, 'rb')

        file_name = name

        file_size = self.get_size(file_obj)
        file_obj.close()
        total_chunks = self.get_total_chucks(chunk_size, file_size)

        LOG.info('reading file to chunks.......')

        for chunk_number, data_size, read_data in self.read_file_to_chunks(file):
            uploaded_chunk = SimpleUploadedFile(
                file_name, read_data, content_type='multipart/form-data')

            data = {
                'batch_id': batch_id,
                'resumable_chunk_number': chunk_number,
                'resumable_chunk_size': chunk_size,
                'resumable_identifier': '%s-%s' % (file_size, file_name),
                'resumable_total_size': file_size,
                'resumable_current_chunk_size': data_size,
                'resumable_filename': file_name,
                'resumable_total_chunks': total_chunks,
            }
            data['file'] = uploaded_chunk
            response = self.client.post('/api/v1/uploads/', data, format='multipart')
            json_response = response.json()
            if json_response['data']['created'] is True:
                self.assertEqual(response.status_code, 201)
                subject = 'InterVenn file uploaded'
                self.assertEqual(self.check_for_email_notification(subject), True)
            else:
                self.assertEqual(response.status_code, 200)

    @staticmethod
    def check_for_email_notification(subject=None):
        """
        Check for email notification
        """
        for row in mail.outbox:
            if subject in list(map(lambda x: x.subject, mail.outbox)):
                return True
        return False

    def create_batch(self, name):
        """
        create batch
        """
        data = {'name': name}
        response = self.client.post(
            '/api/v1/batches/', data=json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        return response.json()

    def test_resumable_upload(self):
        """
        test resumable upload
        """
        name = 'TestBatch'
        json_response = self.create_batch(name)
        batch_id = json_response['data']['uuid']
        file_name='test_file_upload'
        self.upload_a_file(file_name, batch_id, size_in_mb=10)
        upload = Upload.objects.find_by_name(file_name)
        self.assertEqual(upload.valid, True)


    def test_filter_file_name_upload(self):
        """
        Test filter file name
        """
        response = self.client.get(
            '/api/v1/uploads/?filter[file_name]=test_file_upload_1', format='json')

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['data'][0]['id'], 1)

    def test_filter_id_upload(self):
        """
        Test filter file name
        """
        response = self.client.get(
            '/api/v1/uploads/?filter[id]=2', format='json')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['data'][0]['id'], 2)

    def test_patch_upload(self):
        """
        test patch upload
        """
        response = self.client.get(
           '/api/v1/uploads/?filter[file_name]=test_file_upload_3', format='json')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['data'][0]['id'], 3)
        uuid = json_response['data'][0]['uuid']


        data = {'name': 'test_file_upload_3_updated'}
        response = self.client.patch(
            '/api/v1/uploads/%s' % uuid,
            json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)


        response = self.client.get('/api/v1/uploads/%s' % uuid, format='json')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['data']['uuid'], uuid)
        self.assertEqual(json_response['data']['file_name'], data['name'])
