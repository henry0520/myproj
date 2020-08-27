"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

batch.urls
"""
from django.conf.urls import url
from .views import upload_views

urlpatterns = [
    url(r'^api/v1/uploads/?$', upload_views.UploadView.as_view()),
    url(r'^api/v1/uploads/(?P<uuid>[0-9A-Fa-f-]+)/?$', upload_views.UploadUUIDView.as_view()),
    url(
        r'^api/v1/uploads/(?P<uuid>[0-9A-Fa-f-]+)/download/?$',
        upload_views.DownloadView.as_view(), name='uploaded-download'),
]
