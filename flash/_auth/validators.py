import re

from rest_framework import serializers

from flash._auth.models import MyUser

PHONE_NUMBER_PATTERN = re.compile('^[0-9]{11}$')


# Ensure that user role is courier's
def courier_role_validator(value):
    if value != 4:
        raise serializers.ValidationError('User role is not courier')


# Ensure that user role is client's
def client_role_validator(value):
    if value != 3:
        raise serializers.ValidationError('User role is not client')


def manager_role_validator(value):
    if value != 2:
        raise serializers.ValidationError('User role is not manager')
        

# Ensure that phone number is right format
def phone_number_validator(value):
    if len(value) != 11:
        raise serializers.ValidationError('Phone number must be 11 characters')

    if not PHONE_NUMBER_PATTERN.match(value):
        raise serializers.ValidationError('Phone number is invalid')


# Ensure than role exists
# In fact not necessary because of Django natural validator
def wrong_role(value):
    result = False

    for el in MyUser.USER_ROLES:
        if value == el[0]:
            return

    if not result:
        raise serializers.ValidationError('Role not found')
