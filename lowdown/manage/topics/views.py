from rest_framework import filters

from lowdown.core.topics.models import Topic
from .serializers import TopicSerializer
from rest_framework import generics


class RetrieveUpdateDestroyTopic(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class ListCreateTopic(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug')

    def get_queryset(self):
        queryset = Topic.objects.all()

        if 'vertical' in self.kwargs:
            queryset = queryset.filter(section__vertical=self.kwargs['vertical'])
        return queryset
