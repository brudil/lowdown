from lowdown.core.sections.models import Section
from rest_framework import serializers


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'created',
            'updated',
            'title',
            'slug',
            'parent',
            'deleted',
        )
