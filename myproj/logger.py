"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API myproj.logger
"""

import logging
import logging.handlers

def get_logger(name=None, base='myproj'):
    """
    get logger
    """
    if not name:
        return logging.getLogger(base)
    return logging.getLogger("%s.%s" % (base, name))
