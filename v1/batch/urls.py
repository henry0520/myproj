"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

batch.urls
"""
from django.conf.urls import url
from .views import batch_views

urlpatterns = [
    url(r'^api/v1/batches/?$', batch_views.BatchView.as_view()),
    url(r'^api/v1/batches/(?P<uuid>[0-9A-Fa-f-]+)/?$', batch_views.BatchUUIDView.as_view()),
]
