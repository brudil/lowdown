from config.serializers import TagListSerializer
from lowdown.core.multimedia.models import Multimedia, MultimediaImage
from rest_framework import serializers


class MultimediaImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultimediaImage
        fields = (
            'focus_point_x',
            'focus_point_y',
            'width',
            'height',
        )

        read_only_fields = (
            'width',
            'height',
        )


class MultimediaChildModelField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, MultimediaImage):
            serializer = MultimediaImageSerializer(value)
        else:
            raise Exception('Unexpected multimedia child object')

        return serializer.data


class MultimediaSerializer(serializers.ModelSerializer):
    tags = TagListSerializer()
    type_data = MultimediaChildModelField(source='media_object', read_only=True)

    class Meta:
        model = Multimedia
        read_only_fields = (
            'id',
            'created',
            'updated',
            'hash',
            'resource_name',
            'direct_url',
            'file_name',
            'file_type',
            'mime',
            'source_method',
            'metadata',
            'uploader',
            'deleted',
            'type_data'
        )
        fields = (
            'id',
            'created',
            'updated',
            'hash',
            'resource_name',
            'direct_url',
            'file_name',
            'file_type',
            'mime',
            'credit_title',
            'credit_url',
            'source_method',
            'metadata',
            'uploader',
            'tags',
            'deleted',
            'type_data'
        )
