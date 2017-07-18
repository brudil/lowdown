import django_filters
from lowdown.core.users.models import LowdownUser
from .serializers import UserSerializer
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import api_view

from rest_framework.response import Response


@api_view(['GET', ])
def detail_current_user(request):
    return Response(UserSerializer(request.user).data)

#
# class UsersFilter(filters.FilterSet):
#     username = django_filters.CharFilter()
#     first_name = django_filters.CharFilter()
#     last_name = django_filters.CharFilter()
#
#     class Meta:
#         model = LowdownUser


class ListUsers(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = LowdownUser.objects.all()
    # filter_class = UsersFilter
    search_fields = ('username', 'first_name', 'last_name')
