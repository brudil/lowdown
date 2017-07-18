from lowdown.core.series.models import Series
from .serializers import SeriesSerializer
from rest_framework import generics


class RetrieveUpdateDestroyTopic(generics.RetrieveUpdateDestroyAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class ListCreateTopic(generics.ListCreateAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
