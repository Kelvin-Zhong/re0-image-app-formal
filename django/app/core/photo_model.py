from django.db import models
from django.conf import settings

import uuid
import os


FACIAL_EXPRESSION_TYPES = [
    ['HAPPY', 'HAPPY'],
    ['UNHAPPY', 'UNHAPPY'],
    ['UNKNOWN', 'UNKNOWN']
]


class FacialExpressionType(object):
    HAPPY = 'HAPPY'
    UNHAPPY = 'UNHAPPY'
    UNKNOWN = 'UNKNOWN'


def photo_directory_path(instance):
    return os.path.join('uploads/',
                        str(instance.user.id) + '/',
                        'photo/')


def photo_image_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    # check image formats
    if ext not in ['jpg', 'jpeg', 'png']:
        raise ValueError('image file not valid')
    filename = f'image.{ext}'
    return os.path.join(photo_directory_path(instance), filename)


class PhotoBase(models.Model):
    """Photo object posted by the user"""

    class Meta:
        abstract = True

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    image = models.ImageField(
        null=True,
        upload_to=photo_image_file_path)

    facial_expression_type = models.CharField(
        default=FacialExpressionType.UNKNOWN,
        choices=FACIAL_EXPRESSION_TYPES,
        max_length=100)

