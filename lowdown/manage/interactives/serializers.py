from config.serializers import TagListSerializer
from lowdown.core.interactives.models import Interactive, InteractiveRelease
from rest_framework import serializers


class InteractiveSerializer(serializers.ModelSerializer):
    latest_public_release_number = serializers.SerializerMethodField()

    class Meta:
        model = Interactive
        fields = (
            'id',
            'revision_count',
            'slug',
            'latest_public_release_number',
        )

        read_only_fields = (
            'id',
            'revision_count',
            'latest_public_release_number',
        )

    def get_latest_public_release_number(self, obj):
        return obj.get_latest_public_release().revision_number


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
