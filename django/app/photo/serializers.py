from rest_framework import serializers

from core.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    """Serialize a photo object"""

    class Meta:
        model = Photo
        fields = (
            'id',
            'facial_expression_type',
            'created_time',
            'user',
            'image',
        )
        read_only_fields = ('id', 'created_time')
        extra_kwargs = {'user': {'read_only': True}}