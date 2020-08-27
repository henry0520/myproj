"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API utils.swagger_schema
"""

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.schemas import SchemaGenerator, AutoSchema
from urllib.parse import urljoin
from collections import Counter, OrderedDict
import yaml
import coreapi
from six.moves.urllib import parse as urlparse

class LinkNode(OrderedDict):
    def __init__(self):
        self.links = []
        self.methods_counter = Counter()
        super(LinkNode, self).__init__()

    def get_available_key(self, preferred_key):
        if preferred_key not in self:
            return preferred_key

        while True:
            current_val = self.methods_counter[preferred_key]
            self.methods_counter[preferred_key] += 1

            key = '{}_{}'.format(preferred_key, current_val)
            if key not in self:
                return key

class CustomViewSchema(AutoSchema):
    def get_link(self, path, method, base_url, view=None):
        fields = self.get_path_fields(path, method)
        yaml_doc = None
        if self._view and self._view.__doc__:
            try:
                yaml_doc = yaml.load(self._view.__doc__)
            except Exception as e:
                print(e)
                yaml_doc = None

        #Extract schema information from yaml
        if yaml_doc and type(yaml_doc) != str:
            _method_desc = yaml_doc.get('description', '')
            params = yaml_doc.get('parameters', [])

            for i in params:
                _name = i.get('name')
                _desc = i.get('description')
                _required = i.get('required', False)
                _type = i.get('type', 'string')
                _location = i.get('location', 'form')
                field = coreapi.Field(
                    name=_name,
                    location=_location,
                    required=_required,
                    description=_desc,
                    type=_type
                )
                fields.append(field)
        else:

            _method_desc = view.__doc__ if view and view.__doc__ else ''
            fields += self.get_serializer_fields(path, method)

        fields += self.get_pagination_fields(path, method)
        fields += self.get_filter_fields(path, method)

        manual_fields = self.get_manual_fields(path, method)
        fields = self.update_fields(fields, manual_fields)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method)
        else:
            encoding = None

        description = self.get_description(path, method)

        if base_url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urlparse.urljoin(base_url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=description
        )


class CustomSchemaGenerator(SchemaGenerator):
    def get_link(self, path, method, view):
        fields = self.get_path_fields(path, method, view)
        yaml_doc = None
        if view and view.__doc__:
            try:
                yaml_doc = yaml.load(view.__doc__)
            except:
                yaml_doc = None

        #Extract schema information from yaml

        if yaml_doc and type(yaml_doc) != str:
            _method_desc = yaml_doc.get('description', '')
            params = yaml_doc.get('parameters', [])

            for i in params:
                _name = i.get('name')
                _desc = i.get('description')
                _required = i.get('required', False)
                _type = i.get('type', 'string')
                _location = i.get('location', 'form')
                field = coreapi.Field(
                    name=_name,
                    location=_location,
                    required=_required,
                    description=_desc,
                    type=_type
                )
                fields.append(field)
        else:

            _method_desc = view.__doc__ if view and view.__doc__ else ''
            fields += self.get_serializer_fields(path, method, view)

        fields += self.get_pagination_fields(path, method, view)
        fields += self.get_filter_fields(path, method, view)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, view)
        else:
            encoding = None

        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=_method_desc
        )

