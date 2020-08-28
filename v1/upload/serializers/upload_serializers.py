"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API batch.serializers.batch_serializers
"""
from myproj import logger

from rest_framework import serializers
from django.http import HttpResponse
from django.utils import timezone

# tasks
from tasks.upload import notification as notification_task

# models
from models.upload.models import Upload
from models.batch.models import Batch

LOG = logger.get_logger(__name__)

class UploadShortSerializer(serializers.ModelSerializer):
    """
    upload model serializers short version
    """
    uploaded_chunks = serializers.SerializerMethodField()

    @staticmethod
    def get_uploaded_chunks(obj):
        """
        return the list of uploaded chucks
        """
        return list(obj.uploaded_chunks.keys())

    class Meta:
        """
        serializer meta options
        """
        model = Upload
        fields = ['valid', 'uploaded_chunks', 'uploaded_size']

class ResumableUploadSerializer(serializers.Serializer):
    """
    resumable upload serializer
    """
    batch_id = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        max_length=36,
        error_messages={
            'required': 'Batch id is required',
            'null': 'Batch id should not be null',
            'blank': 'Batch id should not be blank',
            'max_length': 'Batch id should not be greater than 36 characters',
        })

    resumable_chunk_number = serializers.IntegerField(
        error_messages={
            'required': 'Resumable chunk number is required',
            'blank': 'Resumable chunk number is required',
            'null': 'Resumable chunk number is required',
        })
    resumable_chunk_size = serializers.IntegerField(
        error_messages={
            'required': 'Resumable chunk size is required',
            'blank': 'Resumable chunk size is required',
            'null': 'Resumable chunk size is required',
        })

    resumable_identifier = serializers.CharField(
        max_length=254,
        error_messages={
            'max_length': 'Resumable identifier should not be greater than 254'\
                'characters',
            'required': 'Resumable identifier is required',
            'blank': 'Resumable identifier is required',
            'null': 'Resumable identifier is required',
        })
    resumable_total_size = serializers.IntegerField(
        error_messages={
            'required': 'Resumable total size is required',
            'blank': 'Resumable total size is required',
            'null': 'Resumable total size is required',
        })
    resumable_current_chunk_size = serializers.IntegerField(
        error_messages={
            'required': 'Resumable current chunk size is required',
            'blank': 'Resumable current chunk size is required',
            'null': 'Resumable current chunk size is required',
        })
    resumable_filename = serializers.CharField(
        error_messages={
            'required': 'Resumable filename is required',
            'blank': 'Resumable filename is required',
            'null': 'Resumable filename is required',
        })
    resumable_total_chunks = serializers.IntegerField(
        error_messages={
            'required': 'Resumable total chunks is required',
            'blank': 'Resumable total chunks is required',
            'null': 'Resumable total chunks is required',
        })
    file = serializers.FileField(
        error_messages={
            'required': 'File is required',
            'blank': 'File is required',
            'null': 'File is required',
        },
        style={'input_type': 'file'}
    )

    def validate_batch_id(self, batch_id):
        """
        validate batch id
        """
        if not self.batch_instance:
            raise serializers.ValidationError('Batch uuid does not exist')
        return batch_id

    @property
    def batch_instance(self):
        """
        Batch instance
        """
        request = self.context.get('request')
        return Batch.objects.find_by_uuid(request.data.get('batch_id'))

    def get_or_create_upload_from_request(self, request):
        """
        get or create upload from request
        """
        name = request.data['resumable_filename']
        file_id = request.data['resumable_identifier']
        instance, _ = Upload.objects.get_or_create(
            user=request.user,
            file_id=file_id,
            batch=self.batch_instance,

            defaults={'name': name}
        )
        return instance, _

    def save(self):
        """
        save
        """
        request = self.context.get('request', None)
        if self.is_test_request(request):
            return self.check_chunk_status(request)
        try:
            upload, created = self.consume(request)
        except AssertionError as err:
            LOG.exception(err)
            return {
                'status': 'ERROR',
                'error_message': "Uploaded size > total size.",
                'error_type': 'ApiError'
            }
        except Exception as err:
            upload = Upload.objects.get(
                batch__uuid=request.data.get('batch_id'),
                user=request.user,
                file_id=request.data.get('resumable_identifier'))
            upload.delete()
            return {'status': 'ERROR', 'error_message': str(err), 'error_type': 'ApiError'}

        return {
            'status':'OK',
            'created': created,
            'upload': UploadShortSerializer(upload).data
        }

    @staticmethod
    def check_chunk_status(request):
        """
        This always return HTTP 204
        """
        if False:
            return HttpResponse(status=200)
        return HttpResponse(status=204)

    @staticmethod
    def is_test_request(request):
        """
        is test request
        """
        return request.method == 'GET'

    def seek(self, request, f):
        """
        seek
        """
        chunk_size = int(request.data['resumable_chunk_size'])
        offset = (int(request.data['resumable_chunk_number']) - 1) * chunk_size
        LOG.debug('seking chunk, size:%s offset:%s', chunk_size, offset)
        f.seek(offset)
        assert f.tell() == offset
        return f

    def consume(self, request, **kwargs):
        """
        consume
        """
        upload_instance, _ = self.get_or_create_upload_from_request(request)
        uploaded_file = None
        if request.data.get('file', None):
            uploaded_file = request.data['file']
        elif request.FILES:
            uploaded_file = request.FILES['file']

        if uploaded_file:
            with self.seek(request, upload_instance.open()) as file_object:
                data = uploaded_file.read()
                file_object.write(data)

            resumable_chunk_number = request.data['resumable_chunk_number']
            resumable_chunk_size = request.data['resumable_chunk_size']
            resumable_current_chunk_size = request.data['resumable_current_chunk_size']
            resumable_total_size = request.data['resumable_total_size']

            offset = (int(resumable_chunk_number) - 1) * int(resumable_chunk_size)
            uploaded_size = offset + int(resumable_current_chunk_size)
            total_size = int(resumable_total_size)

            assert uploaded_size <= total_size

            uploaded_data = {
                'chunk_number': resumable_chunk_number,
                'uploaded_size': uploaded_size,
                'uploaded_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')
            }
            upload_instance.update_chunks_data(uploaded_data)
            if uploaded_size == total_size:
                upload_instance.content_type = upload_instance.c_type
                upload_instance.valid = True
                upload_instance.save()
                notification_task.uploaded.apply_async([upload_instance, request.get_host()])
                return upload_instance, True
            return upload_instance, False


class PatchUploadSerializer(serializers.ModelSerializer):
    """
    patch upload serializer
    """
    name = serializers.CharField(
        max_length=250,
        error_messages={
            'max_length': 'Name should not be greater than 250 characters',
            'required': 'Name is required',
            'blank': 'Name should not be blank',
            'null': 'Name should not be null',
        })
    class Meta:
        """
        Upload serializer meta options
        """
        model = Upload
        fields = ('id', 'uuid', 'name', 'date_created', 'content_type', 'path',)
        read_only_fields = ('id', 'uuid', 'date_created', 'path')


class UploadSerializer(serializers.Serializer):
    """
    upload serializer
    """
    id = serializers.IntegerField(read_only=True)
    uuid = serializers.CharField(read_only=True)
    file_name = serializers.SerializerMethodField()
    content_type = serializers.CharField()
    download_url = serializers.SerializerMethodField()
    date_created = serializers.DateTimeField()

    def get_file_name(self, obj):
        """
        get file name
        """
        return obj.name

    def get_download_url(self, obj):
        """
        get download url
        """
        if isinstance(self.instance, Upload):
            return self.instance.download_link
        return obj.download_link

    class Meta:
        """
        Upload serializer meta options
        """
        fields = ('id', 'uuid', 'name', 'date_created', 'content_type', 'path',)
        read_only_fields = ('id', 'uuid', 'date_created',)
