from lowdown.core.authors.models import Author
from .serializers import AuthorSerializer
from rest_framework import generics


class ListAuthors(generics.ListAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    search_fields = ('name', )
