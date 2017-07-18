from lowdown.core.sections.models import Section
from lowdown.core.topics.models import Topic
from lowdown.manage.topics.serializers import TopicSerializer
from .serializers import SectionSerializer
from rest_framework import generics


class RetrieveUpdateDestroySection(generics.RetrieveUpdateDestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class ListTopicsForSection(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(section=self.kwargs['pk'])


class ListCreateSection(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_queryset(self):
        return Section.objects.filter(vertical=self.kwargs['vertical'])

    def perform_create(self, serializer):
        serializer.save(vertical=self.kwargs['vertical'])
