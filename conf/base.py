"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API base settings
"""
import os
import sys
import base64
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.normpath(os.path.dirname(__file__))

STATIC_ROOT = os.path.join(BASE_DIR, 'static') + '/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
