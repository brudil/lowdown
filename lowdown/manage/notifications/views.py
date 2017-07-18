from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', ])
def stub_count(request):
    return Response(dict(count=3))
