"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API conf.logging
"""

import logging
# base dir and settings path
from .base import os, sys

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s \
                %(process)d %(thread)d %(message)su'
        },
        'default': {
            'format': '%(asctime)s %(levelname)s %(filename)s \
                %(lineno)d - %(message)s'
        },
    },
    'handlers': {
        'null': {
             'class': 'logging.NullHandler',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': sys.stdout,
        },
        'log_to_stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'facility': 'local1',
            'address': '/dev/log',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'main': {
            'handlers': ['syslog', 'log_to_stdout'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['log_to_stdout'],
            'level': 'ERROR',
            'propagate': False
        },
        'myproj': {
            'handlers': ['console', 'log_to_stdout'],
            'level': 'INFO',
            'propagate': False
        },
    },
    'root': {
        'handlers': ['log_to_stdout'],
        'level': 'INFO'
    }
}
