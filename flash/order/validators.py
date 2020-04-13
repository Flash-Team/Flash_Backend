from rest_framework import serializers


# Ensure that count of product is positive
def positive_number_validator(value):
    if value < 0:
        raise serializers.ValidationError('Count must be positive')


# Ensure that value of rating is between 0 and 5
def rating_validator(value):
    if value > 5 or value <= 0:
        raise serializers.ValidationError('Invalid rating value')
