from lowdown.core.multimedia.models import Multimedia
from lowdown.manage.users.serializers import UserSerializer
from rest_framework import serializers


class MultimediaImageSerializer(serializers.ModelSerializer):
    width = serializers.IntegerField(source='media_object.width')
    height = serializers.IntegerField(source='media_object.height')

    class Meta:
        model = Multimedia
        fields = (
            'id',
            'resource_name',
            'file_type',
            'credit_title',
            'credit_url',
            'width',
            'height',
        )
