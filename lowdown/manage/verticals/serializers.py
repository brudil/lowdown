from rest_framework import serializers


class VerticalSerializer(serializers.Serializer):
    name = serializers.CharField()
    identifier = serializers.CharField()
    content_forms = serializers.ListField(child=serializers.IntegerField())
    content_tones = serializers.ListField(child=serializers.IntegerField())
