"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

Task upload notification

"""
from django.core.mail import send_mail
from myproj import logger
from ..decorators import task

LOG = logger.get_logger(__name__)

@task
def uploaded(instance, **kwargs):
    """
    uploaded
    """
    LOG.info(instance.content_type)
    subject = 'InterVenn file uploaded'
    message = """
        Hi There,

        Someone sent you a file(s).

        To download the file click on - https://localtest.com/api/v1/batches/%s

        Best Regards,

        InterVenn
    """ % instance.batch.uuid

    send_mail(
       subject, message, 'developers@intervenn.com', 
       ['henz.jmedina@gmail.com'], fail_silently=False)
    LOG.info('Email sent')
