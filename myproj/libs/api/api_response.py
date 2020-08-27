"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

Jsonapi.org compliant api response
"""

import json
import decimal
import uuid
import datetime
import six

from django.http import HttpResponse
from django.utils.functional import Promise
from django.utils.duration import duration_iso_string
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from myproj.libs.templates.helpers import dttime_format

class JSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types, and
    UUIDs.
    """
    def default(self, o):

        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            return dttime_format(o)
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, datetime.time):
            if timezone.is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            result = o.isoformat()
            if o.microsecond:
                result = result[:12]
            return result
        if isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        if isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
            return str(o)
        return super().default(o)

class ApiResponse:
    """
    Api Response base class
    """
    def __init__(self, status=200, headers=None,
                 content_type='application/vnd.api+json',
                 request=None):
        """
        define attributes on init
        """
        self.status = status
        self.headers = headers
        self.content_type = content_type
        self.request = request

    def set_status(self, status):
        """
        status attribute setter
        """
        self.status = status

    def get_status(self):
        """
        status attribute getter
        """
        return self.status

    def get_headers(self):
        """
        header attrib getter
        """
        return self.headers

    def get_content_type(self):
        """
        content_type attrib getter
        """
        return self.content_type

    def get_success_data(self, data, meta, links):
        """
        jsonapi specs for succesful data
        """
        return {
            "data": data,
            "meta": meta,
            "links": links,
            "status": self.get_status(),
        }

    def get_error_data(self, data, message):
        """
        jsonapi specs for validation errors
        """
        errors = []
        if data:
            if isinstance(data, (ReturnDict, dict)):
                for key, val in data.items():
                    if isinstance(val, list):
                        val = "".join(val)

                    errors.append({
                        "title": message,
                        "detail": val,
                        "source": {"pointer": "/data/attributes/%s" % key},
                    })
            elif isinstance(data, (ReturnList, list)):
                errors = self._get_returnlist_errors(data, errors)

        return {"errors": errors, "status": self.get_status()}


    def _get_returnlist_errors(self, data, errors):
        """
        handle ReturnList, list type of data
        """
        for err in data:
            if 'message' in err and isinstance(err['message'], ErrorDetail):
                try:
                    field = err['message'].split(':')[1].strip()
                except IndexError:
                    field = err['message']
                errors.append({
                    'title': err['message'].code,
                    'detail': err['message'],
                    "source": {"pointer": "/data/attributes/%s" % field},
                })


        return errors


    def success(self, data=None, meta=None, links=None):
        """
        HTTP 200 response
        """
        self.set_status(200)
        response_data = self.get_success_data(
            data=data, meta=meta, links=links)

        return self.api_response(response_data)


    def created(self, data=None, meta=None, links=None):
        """
        HTTP 201 response
        """
        self.set_status(201)
        response_data = self.get_success_data(
            data=data, meta=meta, links=links)

        return self.api_response(response_data)

    def api_response(self, data):
        """
        generic api response
        """

        response = HttpResponse(
            json.dumps(data, cls=JSONEncoder),
            content_type=self.content_type,
            status=self.status)
        if self.headers:
            for key, value in six.iteritems(self.headers):
                response[key] = value

        return response

    def bad_gateway(self, data=None, message="Bad Gateway"):
        """
        HTTP 502
        """
        self.set_status(502)
        response_data = self.get_error_data(data, message)

        return self.api_response(response_data)

    def bad_request(self, data=None, message="Bad Request", errors=None):
        """
        HTTP 500
        """
        self.set_status(400)
        if errors is None:
            response_data = self.get_error_data(data, message)

        # This else statement has no use yet commenting it for now (SCS-598)
        #else:
        #    response_data = self.set_error_response(errors)

        return self.api_response(response_data)

    def unprocessable_entity(self, data=None, message="Unprocessable Entity"):
        """
        HTTP 422
        """
        self.set_status(422)
        response_data = self.get_error_data(data, message)

        return self.api_response(response_data)

    def unauthorized(self, data=None, message="Unauthorized"):
        """
        HTTP 401
        """
        self.set_status(401)
        response_data = self.get_error_data(data, message)

        return self.api_response(response_data)

    def forbidden(self, data=None, message="Forbidden"):
        """
        HTTP 403
        """
        self.set_status(403)
        response_data = self.get_error_data(data, message)

        return self.api_response(response_data)

    def not_found(self, data=None, message="Not Found"):
        """
        HTTP 404
        """
        self.set_status(404)
        response_data = self.get_error_data(data, message)

        return self.api_response(response_data)


    def no_content(self, data=None, meta=None, links=None):
        """
        HTTP 204
        response for DELETE method
        """
        self.set_status(204)
        response_data = self.get_success_data(data=data, meta=meta, links=links)
        return self.api_response(response_data)

    def internal_server_error(self, data=None, message="Internal Server Error"):
        """
        HTTP 500
        """
        self.set_status(500)
        response_data = self.get_error_data(data, message)

        return self.api_response(response_data)

    def method_not_allowed(self, data=None, message="Method Not Allowed"):
        """
        HTTP 405
        """
        self.set_status(405)
        response_data = self.get_error_data(data, message)

        return self.api_response(response_data)
