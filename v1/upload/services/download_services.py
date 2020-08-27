"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API upload related services
"""
import mimetypes
import urllib

# django
from django.http import StreamingHttpResponse

# logger
from myproj import logger

# models
from models.upload.models import Upload

# libs
from myproj.libs.services.base import BaseService

# utils
from myproj.utils.handler.exception import NotFound

class DownloadService(BaseService):
    """
    download service
    """
    def process_download(self):
        """
        get stores and put it in zip stream
        """
        self.data = self.instance.retrieve()

    def prepare_download(self):
        """
        configure response for file stream download
        """
        if self.instance.content_type is not None:
            mimetype, encoding = mimetypes.guess_type(self.instance.name)
            mimetype = self.instance.content_type
        else:
            mimetype, encoding = mimetypes.guess_type(self.instance.name)

        response = StreamingHttpResponse(self.data, content_type=str(mimetype))

        if encoding is not None:
            response['Content-Encoding'] = encoding

        # To inspect details for the below code,
        # see http://greenbytes.de/tech/tc2231/
        if 'WebKit' in self.request.META.get('HTTP_USER_AGENT', ''):
            # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
            filename_header = 'filename="%s"' % self.instance.download_filename
        elif 'MSIE' in self.request.META.get('HTTP_USER_AGENT', ''):
            # IE does not support internationalized filename at all.
            # It can only recognize internationalized URL,
            # so we do the trick via routing rules.
            filename_header = ''
        else:
            # For others like Firefox, we follow RFC2231
            # (encoding extension in HTTP headers).
            filename_header = 'filename*=UTF-8\'\'{0}'.format(
                urllib.parse.quote(self.instance.download_filename)
            )

        response['Content-Disposition'] = 'attachment; ' + filename_header
        return response

    def get_queryset(self):
        """
        get queryset
        """
        instance = Upload.objects.find_by_uuid(self.uuid)
        if not instance:
            self.errors={'instance': 'Invalid Instance'}
            raise NotFound
        return instance

    def run(self):
        """
        run service
        """
        self.instance = self.get_queryset()
        self.process_download()
        response = self.prepare_download()
        return response
