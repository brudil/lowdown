from rest_framework.response import Response

from lowdown.core.verticals.structure import MANAGER
from .serializers import VerticalSerializer
from rest_framework import views


class ListVerticals(views.APIView):

    def get(self, request):
        return Response(VerticalSerializer(MANAGER.verticals, many=True).data)
