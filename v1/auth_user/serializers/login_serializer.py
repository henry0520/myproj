"""
********************************************************

© YYYY - 2020 InterVenn. All Rights Reserved.

********************************************************

API auth_user.serializers.login_serializer
"""

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """
    Login Serializer

    Parameters:
    email (string) email
    password (string) password

    Returns:
    (dictionary) data
    (dictionary) errors
    """
    email = serializers.EmailField(
        error_messages={
            'required': 'Email is required',
            'blank': 'Email is required',
            'null': 'Email is required',
        },
        style={
            'input_type': 'email'
        })

    password = serializers.CharField(
        error_messages={
            'required': 'Password is required',
            'blank': 'Password is required',
            'null': 'Password is required',
        },
        style={
            'input_type': 'password'
        })

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
