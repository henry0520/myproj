"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

v1.urls endpoint
"""
from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('v1.batch.urls')),
    url(r'^', include('v1.upload.urls')),
    url(r'^', include('v1.auth_user.urls')),
]
