import os
from django.core.exceptions import ValidationError
from rest_framework import serializers

MAX_FILE_SIZE = 1024000
ALLOWED_EXTENSIONS = ['.jpg', '.png', '.img']


def validate_file_size(value):
    """
    Validator for checking max size of the file.
    In case, if it is bigger than MAX_FILE_SIZE,
    error will appear

    """
    if value.size > MAX_FILE_SIZE:
        raise ValidationError(f'File size error! Max file size is: {MAX_FILE_SIZE}')


def validate_extension(value):
    """
    Validator for checking file extension.
    .png, .jpg, .img are only allowed

    """
    split_ext = os.path.splitext(value.name)
    if len(split_ext) > 1:
        ext = split_ext[1]
        if not ext.lower() in ALLOWED_EXTENSIONS:
            raise ValidationError(f'File extension error! Valid extensions are: {ALLOWED_EXTENSIONS}')


def rating_validator(value):
    """
    Checks whether value is in the range between [0; 5)

    """
    if value > 5 or value <= 0:
        raise serializers.ValidationError('Invalid rating value')
