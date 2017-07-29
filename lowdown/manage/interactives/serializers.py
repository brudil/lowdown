from config.serializers import TagListSerializer
from lowdown.core.interactives.models import Interactive, InteractiveRelease
from rest_framework import serializers


class InteractiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interactive
        fields = (
            'id',
            'revision_count',
            'slug'
        )

        read_only_fields = (
            'id',
            'revision_count',
        )


class InteractiveReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractiveRelease
        read_only_fields = (
            'id',
            'created',
            'revision_number',
            'interactive',
        )
        fields = (
            'id',
            'created',
            'revision_number',
            'interactive',
            'public'
        )
