"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************

auth_user.models
"""

# django
from django.contrib.auth.models import User as AuthUser

# managers
from .managers.user_manager import UserManager

class User(AuthUser):
    """
    Extends default django User model
    """
    objects = UserManager()
    class Meta:
        """
        model meta options
        """
        proxy = True

    def natural_key(self):
        """
        set email as natural key
        """
        return (self.email,)

    def __str__(self):
        """
        string representation
        """
        return self.email
