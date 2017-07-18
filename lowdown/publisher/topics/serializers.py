from lowdown.core.topics.models import Topic
from rest_framework import serializers


class MinimalTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = (
            'id',
            'title',
            'slug',
        )
