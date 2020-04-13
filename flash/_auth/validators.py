from rest_framework import serializers


# Ensure that user role is courier's
def courier_role_validator(value):
    if value != 4:
        raise serializers.ValidationError('User role is not courier')


# Ensure that user role is client's
def client_role_validator(value):
    if value != 3:
        raise serializers.ValidationError('User role is not client')


