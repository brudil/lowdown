from django.contrib.auth.models import Permission

from lowdown.core.users.models import LowdownUser
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ('key', )

    def get_key(self, obj):
        return '{}.{}'.format(obj.content_type.natural_key()[0], obj.codename)


class UserSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = LowdownUser
        fields = ('id', 'username', 'first_name', 'last_name', 'gravatar_hash', 'permissions')

