from lowdown.core.users.models import LowdownUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = LowdownUser
        fields = ('id', 'username', 'first_name', 'last_name', 'gravatar_hash')
