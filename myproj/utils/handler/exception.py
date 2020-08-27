"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API utils.handler.exception
"""

class InvalidInput(Exception):
    """
    invalid input
    """
    def __init__(self, message='Invalid input'):
        super(InvalidInput, self).__init__(message)

class Unauthorized(Exception):
    """
    unauthorized
    """
    def __init__(self, message='Unauthorized'):
        super(Unauthorized, self).__init__(message)

class NotFound(Exception):
    """
    not found
    """
    def __init__(self, message='Not found'):
        super(NotFound, self).__init__(message)

class ApplicationException(Exception):

    def __init__(self, message='Displayable (expected) exception.'):
        super(ApplicationException, self).__init__(message)
        self.message = message

class ValidationException(ApplicationException):
    """
    validation exception
    """
    def __init__(self, message='Data error.'):
        super(ValidationException, self).__init__(message)
