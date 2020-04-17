from rest_framework import serializers


def rating_validator(value):
    if value > 5 or value <= 0:
        raise serializers.ValidationError('Invalid rating value')
