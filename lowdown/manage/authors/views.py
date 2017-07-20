from lowdown.core.authors.models import Author
from .serializers import AuthorSerializer
from rest_framework import generics


class ListAuthors(generics.ListAPIView):
    serializer_class = AuthorSerializer
    search_fields = ('name', )

    def get_queryset(self):
        queryset = Author.objects.all()

        if 'vertical' in self.kwargs:
            queryset = queryset.filter(vertical=self.kwargs['vertical'])
        return queryset
