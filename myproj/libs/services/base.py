"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API myproj.libs.services.base
"""

class BaseService:
    """
    Base login service
    """
    def __init__(self, **kwargs):
        """
        initialization
        """
        #data
        self.data = kwargs.get('data', {})

        # context
        self.context = kwargs.get('context', {})

        # request
        self.request = kwargs.get('request', None)

        # uuid
        self.uuid = kwargs.get('uuid', None)

        # serializers
        self.serializer = None

        # many
        self.many = True

        # errors
        self.errors = {}

        # instance
        self.instance = None

    def get_queryset(self):
        """
        abstract method, required derived classes to override
        """
        self.errors = {'not_implemented': 'Not Implemented'}
        raise NotImplementedError

    def run(self):
        """
        Run service

        Parameter: self (object)
        Return: (object) instance of domain configuration
        """
        serializer = self.serializer(
            self.get_queryset(),
            many=self.many,
            context={'request': self.request}
        )
        return serializer.data
