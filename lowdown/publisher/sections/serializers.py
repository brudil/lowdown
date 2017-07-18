from lowdown.core.sections.models import Section
from rest_framework import serializers


class MinimalSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'slug',
        )
