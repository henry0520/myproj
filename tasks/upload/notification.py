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
def uploaded(instance, url, **kwargs):
    """
    uploaded
    """
    subject = 'InterVenn file uploaded'
    download_link = "http://{0}/{1}/".format(url, str(instance.batch.uuid))
    message = """
        Hi There,

        Someone sent you a file(s).

        Time uploaded: %s
        Download link: %s

        Best Regards,

        InterVenn
    """ % (instance.date_created.strftime('%Y-%m-%d %H:%M:%S'), download_link)

    send_mail(
       subject, message, 'developers@intervenn.com', 
       ['henz.jmedina@gmail.com', 'lzulaybar@venn.bio', 'mervin@venn.bio'], fail_silently=False)
    LOG.info('Email sent')
