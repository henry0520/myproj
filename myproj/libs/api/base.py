"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************
"""

from django.db.models.query import QuerySet

# rest framework
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.settings import api_settings

# utils
from myproj.utils.swagger_schema import CustomViewSchema

# libs
from .api_response import ApiResponse
from ..paginations.custom_pagination import CustomPagination

# exceptions
from myproj.utils.handler.exception import InvalidInput, \
    NotFound, Unauthorized, ValidationException

# logger
from myproj import logger
LOG = logger.get_logger(__name__)

# A Generic Serializer to use for Views which inherently don't have
# or need serializers
class ObjectSerializer(serializers.BaseSerializer):
    """
    A read-only serializer that coerces arbitrary complex objects
    into primitive representations.
    """
    def to_internal_value(self, data):
        """
        Bypass internal value
        """
        return data

    def to_representation(self, obj):
        """
        To representation
        """
        output = {}
        for attribute_name in dir(obj):
            attribute = getattr(obj, attribute_name)
            if attribute_name.startswith('_'):
                # Ignore private attributes.
                pass
            elif hasattr(attribute, '__call__'):
                # Ignore methods and other callables.
                pass
            elif isinstance(attribute, (str, int, bool, float, type(None))):
                # Primitive types can be passed through unmodified.
                output[attribute_name] = attribute
            elif isinstance(attribute, list):
                # Recursively deal with items in lists.
                output[attribute_name] = [
                    self.to_representation(item) for item in attribute
                ]
            elif isinstance(attribute, dict):
                # Recursively deal with items in dictionaries.
                output[attribute_name] = {
                    str(key): self.to_representation(value)
                    for key, value in attribute.items()
                }
            else:
                # Force anything else to its string representation.
                output[attribute_name] = str(attribute)

        return output

    def create(self, validated_data):
        """
        Bypass create
        """
        return False

    def update(self, instance, validated_data):
        """
        Bypass update
        """
        return False


class BaseAPIView(APIView, CustomPagination):
    """
    SCS Base API View
    """
    permission_classes = [IsAuthenticated,]
    schema = CustomViewSchema() # <----- Enable use YAML docstrings.
    serializer_class = ObjectSerializer #Swagger uses serializers
    model_class = None # class of a model for GET request method
    #to define the fields to be displayed.

    # service soon to deprecate as we do have the following services for
    # get, post, put, delete and patch

    services_get = None
    services_post = None
    services_put = None
    services_delete = None
    services_patch = None

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    api_response_class = ApiResponse

    #The following function should not be removed from this BaseClase
    #(unless you know what you are doing)
    # get_serializer(), get_serializer_class(), get_serializer_context()
    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_queryset(self):
        """
        get initial queryset
        """
        return self.model_class.objects.all()

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset


    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
        except queryset.model.DoesNotExist:
            raise NotFound

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


    #Base functionality may need to be defined later
    def get(self, request, *args, **kwargs):
        """
        Get method request

        Parameters:
        self (object)
        request (object)
        args (primitive)
        kwargs (dictionary)

        Returns:
        (dictionary) data
        """
        if not self.services_get:
            return self.api_response_class(request=request).method_not_allowed(
                data={'get': 'request (GET) method is not allowed'})

        try:
            context = {}
            context['uuid'] = kwargs.get('uuid')
            context['request'] = request

            service = self.services_get(request=request, context=context, *args, **kwargs)
            data = service.run()

            try:
                if not isinstance(service.instance, QuerySet):
                    return self.api_response_class(request=request).success(data=data)
            except AttributeError:
                # not all service has instance attribute
                return self.api_response_class(request=request).success(data=data)

            if self.model_class is None:
                queryset = self.filter_queryset(service.instance)
            else:
                queryset = self.filter_queryset(self.get_queryset())

        except NotFound:
            return self.api_response_class(request=request).not_found(
                data=service.errors)
        except Unauthorized:
            return self.api_response_class(request=request).unauthorized(
                data=service.errors)
        except InvalidInput:
            response = self.api_response_class(request=request)
            return response.unprocessable_entity(
                data=service.errors)
        except ValidationError as err:
            errors = err.get_full_details()
            response = self.api_response_class(request=request)
            return response.bad_request(data=errors)
        except Exception as err:
            LOG.error('Exception due to: %s', err, exc_info=True)
            return self.api_response_class(request=request).internal_server_error(
                data={'exception': '%s' % err})

        page = self.paginate_queryset(
                request=request, queryset=queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
        else:
            serializer = self.get_serializer([], many=True, context={'request': request})

        paginated_data = self.get_paginated_response(
            data=serializer.data)

        return self.api_response_class().success(
            data=paginated_data.get('data'),
            links=paginated_data.get('link'),
            meta=paginated_data.get('meta'),
        )


    def get_authenticate_header(self, request):
        """
        If a request is unauthenticated, determine the WWW-Authenticate
        header to use for 401 responses, if any.
        """
        authenticators = self.get_authenticators()
        if authenticators:
            for auth in authenticators:
                res = auth.authenticate_header(request)
                if res is not None:
                    return res


    # This is the default POST function.To use default functionality,
    # just need to add "service" value.  This may be overriden
    def post(self, request, *args, **kwargs):
        """
        Post method request

        Parameters:
        self (object)
        request (object)
        args (primitive)
        kwargs (dictionary)

        Returns:
        (dictionary) data
        """
        if not self.services_post:
            return self.api_response_class(request=request).method_not_allowed(
                data={'post': 'request (POST) method is not allowed'})

        try:
            service = self.services_post(
                request=request, data=request.data, *args, **kwargs
            )
            data = service.run()
        except InvalidInput:
            return self.api_response_class(request=request).unprocessable_entity(
                data=service.errors)
        except NotFound:
            return self.api_response_class(request=request).not_found(
                data=service.errors)
        except Unauthorized:
            return self.api_response_class(request=request).unauthorized(
                data=service.errors)
        except ValidationException:
            return self.api_response_class(request=request).forbidden(
                data=service.errors)
        except Exception as err:
            LOG.error('Exception due to: %s', err, exc_info=True)
            return self.api_response_class(request=request).internal_server_error(
                data={'exception': '%s' % err})

        if kwargs.get('created'):
            return self.api_response_class(request=request).created(data=data)
            
        return self.api_response_class(request=request).success(data=data)

    #Base functionality may need to be defined later
    def put(self, request, *args, **kwargs):
        """
        Put method request

        Parameters:
        self (object)
        request (object)
        args (primitive)
        kwargs (dictionary)

        Returns:
        (dictionary) data
        """
        if not self.services_put:
            return self.api_response_class(request=request).method_not_allowed(
                data={'put': 'request (PUT) method is not allowed'})

        try:
            context = {}
            context['uuid'] = kwargs.get('uuid')
            context['request'] = request
            service = self.services_put(
                request=request, context=context, data=request.data, *args, **kwargs)
            data = service.run()
        except NotFound:
            return self.api_response_class(request=request).not_found(
                data=service.errors)
        except InvalidInput:
            return self.api_response_class(request=request).unprocessable_entity(
                data=service.errors)
        except Unauthorized:
            return self.api_response_class(request=request).unauthorized(
                data=service.errors)
        except Exception as err:
            LOG.error('Exception due to: %s', err, exc_info=True)
            return self.api_response_class(request=request).internal_server_error(
                data={'exception': '%s' % err})

        return self.api_response_class(request=request).success(data=data)

    #Base functionality may need to be defined later
    def delete(self, request, *args, **kwargs):
        """
        Delete method request

        Parameters:
        self (object)
        request (object)
        args (primitive)
        kwargs (dictionary)

        Returns:
        (dictionary) data
        """
        if not self.services_delete:
            return self.api_response_class(request=request).method_not_allowed(
                data={'delete': 'request (DELETE) method is not allowed'})

        try:
            context = {}
            context['uuid'] = kwargs.get('uuid')
            context['request'] = request
            service = self.services_delete(
                request=request, context=context, *args, **kwargs
            )
            service.run()
        except NotFound:
            return self.api_response_class(request=request).not_found(
                data=service.errors)
        except Unauthorized:
            return self.api_response_class(request=request).unauthorized(
                data=service.errors)
        except InvalidInput:
            return self.api_response_class(request=request).unprocessable_entity(
                data=service.errors)
        except Exception as err:
            LOG.error('Exception due to: %s', err, exc_info=True)
            return self.api_response_class(request=request).internal_server_error(
                data={'exception': '%s' % err})

        return self.api_response_class(request=request).no_content(data={})


    def patch(self, request, *args, **kwargs):
        """
        PATCH method handler, logic should be put inside the
        self.services_patch class
        """

        if not self.services_patch:
            return self.api_response_class(request=request).method_not_allowed(
                data={'patch': 'request (PATCH) method is not allowed'})

        try:
            service = self.services_patch(request=request, data=request.data, *args, **kwargs)
            data = service.run()

        except NotFound:
            return self.api_response_class(request=request).not_found(
                data=service.errors)
        except Unauthorized:
            return self.api_response_class(request=request).unauthorized(
                data=service.errors)
        except InvalidInput:
            return self.api_response_class(request=request).unprocessable_entity(
                data=service.errors)
        except ValidationException:
            return self.api_response_class(request=request).unprocessable_entity(
                data=service.errors)
        except Exception as err:
            LOG.error('Exception due to: %s', err, exc_info=True)
            return self.api_response_class(request=request).internal_server_error(
                data={'exception': '%s' % err})

        return self.api_response_class(request=request).success(data=data)
