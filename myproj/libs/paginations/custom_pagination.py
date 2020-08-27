"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API libs pagination

"""
# core
from rest_framework.pagination import PageNumberPagination

# logger
from myproj import logger

# libs
from ..urls.query_url import QueryUrl

LOG = logger.get_logger(__name__)

class CustomPagination(PageNumberPagination):
    """
    Custom pagination
    """
    page_query_param = 'page[number]'
    page_size_query_param = 'page[size]'
    max_page_size = 100

    def get_paginated_response(self, data=None):
        """
        get paginated response
        """
        self.parsed = QueryUrl(
            uri=self.request.build_absolute_uri())
        self.count = int(self.page.paginator.count)
        self.limit = int(self.get_page_size(self.request))
        return {
            'data': data,
            'link': {
                'first': self.get_first(),
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'last': self.get_last(),
            },
            'meta': {
                'total-pages': self.page.paginator.num_pages,
                'count': self.count,
                'page_size': self.limit
            },
        }

    def get_first(self):
        """
        Get first
        """
        query_string = 'page[number]=1'
        if self.parsed.dict().get('page[size]'):
            query_string += '&page[size]=%s' % \
                self.parsed.dict()['page[size]']
        if self.query_string():
            query_string += '&%s' % self.query_string()
        return self.request.build_absolute_uri('?%s' % \
            query_string)

    def get_last(self):
        """
        Get last
        """
        query_string = '?page[number]=%s' % self.page.paginator.num_pages
        if self.query_string():
            query_string += '&%s' % self.query_string()
        if self.page.paginator.num_pages:
            return self.request.build_absolute_uri('%s' % query_string)
        return

    def query_string(self):
        """
        query string
        """
        query_string = ''
        try:
            dict_value = dict(
                zip(self.request.GET.keys(), self.request.GET.values()))
            query_string = self.remove_limit_offset(dict_value)
        except Exception as err:
            LOG.error('query string error due to: %s', err, exc_info=True)

        return query_string

    def remove_limit_offset(self, dictionary={}):
        """
        remove limit offset
        """
        limit_offset = {}
        for key, val in dictionary.items():
            if key not in['page[number]']:
                limit_offset['%s' % key] = val
        return self.parsed.urlencode(limit_offset)
