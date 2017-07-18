from lowdown.core.series.models import Series
from rest_framework import serializers


class SeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Series
        fields = (
            'id',
            'created',
            'title',
            'slug',
        )
