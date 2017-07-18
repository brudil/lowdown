from lowdown.core.topics.models import Topic
from rest_framework import serializers


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = (
            'id',
            'created',
            'title',
            'slug',
            'section',
        )
