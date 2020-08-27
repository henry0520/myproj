"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API batch.serializers.batch_serializers
"""

from rest_framework import serializers
from v1.upload.serializers.upload_serializers import UploadSerializer

# models
from models.batch.models import Batch
from models.upload.models import Upload

class BatchSerializer(serializers.ModelSerializer):
    """
    Login Serializer
    """
    name = serializers.CharField(
        error_messages={
            'required': 'Name is required',
            'blank': 'Name should not be blank',
            'null': 'Name should not be null',
        })

    def has_duplicate(self, name):
        """
        has duplicate
        """
        if isinstance(self.instance, Batch):
            instance = Batch.objects.exclude_by_uuid(
                self.instance.uuid).find_by_name(name)
            if instance:
                return True
        else:
            if Batch.objects.find_by_name(name) is not None:
                return True

        return False

    def validate_name(self, name):
        """
        Validate name
        """
        if self.has_duplicate(name) == True:
            raise serializers.ValidationError('Duplicate entry for %s' % name)
        return name

    class Meta:
        """
        Batch serializer meta options
        """
        model = Batch
        fields = ('id', 'uuid', 'name', 'date_created',)
        read_only_fields = ('id', 'uuid', 'date_created',)


class BatchUploadSerializer(BatchSerializer):
    """
    Batch upload serializer
    """
    uploaded_files = serializers.SerializerMethodField()

    def get_uploaded_files(self, obj):
        """
        get uploaded_files
        """
        data = []
        for row in Upload.objects.filter(batch=obj):
            data.append(
                {'id': row.id, 'name': row.name, 'content_type': row.content_type,
                'download_url': row.download_link, 'date_created': row.date_created,})
        return data

    class Meta:
        model = Batch
        fields = ('id', 'uuid', 'name', 'date_created', 'uploaded_files')
