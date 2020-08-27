"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API rest settings
"""

CELERY_IMPORTS = [
'tasks',]
CELERY_IGNORE_RESULT = True # Forcefully ignore task results in production.
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['json','pickle']
CELERY_RESULT_BACKEND = 'amqp'
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_SEND_EVENTS = True
BROKER_CONNECTION_RETRY = True
BROKER_CONNECTION_MAX_RETRIES = None
BROKER_CONNECTION_TIMEOUT = 10
BROKER_HOST = 'localtest'
BROKER_PORT = 5672
BROKER_USER = 'myproj'
BROKER_PASSWORD = 'myproj'
BROKER_VHOST = '//myproj'
CELERYD_LOG_LEVEL = 'WARN'
CELERYBEAT_LOG_LEVEL = 'WARN'

BROKER_URL = "{backend}://{user}:{password}@{host}:{port}{vhost}".format(
    backend=CELERY_RESULT_BACKEND,
    user=BROKER_USER,
    password=BROKER_PASSWORD,
    host=BROKER_HOST,
    port=BROKER_PORT,
    vhost=BROKER_VHOST
)
