"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API rest settings
"""

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myproj.utils.handler.exception_handler.custom_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': \
        'myproj.libs.paginations.custom_pagination.CustomPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S %Z',
}
