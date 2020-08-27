import os
import json
from django.test import override_settings
from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from myproj import logger
LOG = logger.get_logger(__name__)


@override_settings(UPLOAD_DIR='/tmp/test/upload/')
@override_settings(CELERY_ALWAYS_EAGER=True)
class MyTestCase(TestCase):
    """
    Use this to override the default settings above.
    """
@override_settings(UPLOAD_DIR='/tmp/test/upload/')
@override_settings(CELERY_ALWAYS_EAGER=True)
class APITestCases(APITestCase):
    """
    Use this to override the default settings above.
    """
    client = APIClient()

class UploadMixin(MyTestCase):
    """
    resumable upload base class for testing
    """
    def setUp(self):
        """
   
        """
        os.makedirs('/tmp/test/upload', exist_ok=True)

    @staticmethod
    def read_file_to_chunks(filename, chunksize=1024000):
        """
        read file and return a generator of chunk
        based on the chunk size supplied
        """
        file_obj = open(filename, 'rb')
        chunk_number = 0
        while True:
            read_data = file_obj.read(chunksize)
            chunk_number += 1
            if not read_data:
                break
            yield chunk_number, len(read_data), read_data

        file_obj.close()

    @staticmethod
    def get_size(file_obj):
        """
        get size in bytes
        """
        file_obj.seek(0, 2) # move the cursor to the end of the file
        size = file_obj.tell()
        return size

    @staticmethod
    def get_total_chucks(chunk_size, total_size):
        """
        get total chunks of a file
        """
        chunks = 0
        if total_size < chunk_size:
            return 1
        if total_size > chunk_size:
            chunks = int(total_size/chunk_size)
            rem = int(total_size/chunk_size % 1)
            if rem:
                chunks += 1
            return chunks
        return chunks

    @staticmethod
    def create_test_file(fname, size_in_mb=200):
        """
        create file base on the size_in_mb parameter
        """
        f_size = size_in_mb * 1024 * 1024
        fname = fname.split('/')[-1]
        assert os.path.isdir('/tmp/test') == True

        with open('/tmp/test/' + fname, 'wb') as fout:
            fout.write(os.urandom(int(f_size)))

        fout.close()
        return '/tmp/test/' + fname

    def upload_file(self, file_path, size_in_mb=200, chunk_size=None, exists=False,
            file_name=None):
        """
        upload a file via rest
        """
        if chunk_size:
            self.chunk_size = chunk_size
        else:
            self.chunk_size = 1024000

        if exists:
            file_ = file_path
        else:
            file_ = self.create_test_file(file_path, size_in_mb=size_in_mb)

        file_obj = open(file_, 'rb')
        self.file_size = self.get_size(file_obj)
        file_obj.close()

        self.total_chunks = self.get_total_chucks(self.chunk_size, self.file_size)
        data = {
            'size': self.file_size
        }
        if file_name is None:
            file_name = file_path.split('/')[-1]
        for chunk_number, data_size, read_data in self.read_file_to_chunks(file_):
            response = self.do_upload(
                chunk_number,
                data_size,
                read_data,
                file_name
                )
        if response.json()['status'] not in (200, 201):
            return response.json()

        return {
            'name': file_name,
            'size': size_in_mb * 1024 * 1024
        }

    def do_upload(self, chunk_number, data_size, read_data, file_name, batch_id=None):
        """
        custom upload function
        """
        uploaded_chunk = SimpleUploadedFile(
            file_name,
            read_data,
            content_type='multipart/form-data')
        data = {
            'resumable_chunk_number': chunk_number,
            'resumable_chunk_size': self.chunk_size,
            'resumable_identifier': '%s-%s' % (self.file_size, file_name),
            'resumable_total_size': self.file_size,
            'resumable_current_chunk_size': data_size,
            'resumable_filename': file_name,
            'resumable_total_chunks': self.total_chunks,
            'batch_id': batch_id,
        }

        data['file'] = uploaded_chunk

        response = self.client.post(
            '/api/%s/stores/upload/' % VERSION, data, format='multipart'
        )
        json_response = response.json()
        LOG.info(json_response)

        if json_response['data']['created'] is True:
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 200)
        uploaded_chunk.close()
        return response

