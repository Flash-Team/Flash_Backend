from rest_framework import serializers


def positive_number_validator(value):
    """
    Validate that count is positive
    """
    if value < 0:
        raise serializers.ValidationError('Count must be positive')


def rating_validator(value):
    """
    Validate that rating in interval (0, 5]
    """
    if value > 5 or value <= 0:
        raise serializers.ValidationError('Invalid rating value')
