from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from lowdown.core.multimedia.models import Multimedia, MultimediaImage
from .serializers import MultimediaSerializer
from rest_framework import generics


class ListCreateMultimedia(generics.ListAPIView):
    serializer_class = MultimediaSerializer
    queryset = Multimedia.objects.all()
    parser_classes = (MultiPartParser, FormParser,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if 'vertical' in self.kwargs:
            queryset = queryset.filter(vertical=self.kwargs['vertical'], deleted=False)

        ids = self.request.query_params.getlist('ids[]')
        if len(ids) > 0:
            return queryset.filter(pk__in=ids)

        if 'order' in self.request.query_params:
            (*order_value, order_key) = self.request.query_params['order'].split('_')
            order_value = '_'.join(order_value)

            order_props = {
                'updated': 'updated',
                'created': 'created'
            }

            if order_value in order_props:
                queryset = queryset.order_by('{}{}'.format('-' if order_key == 'desc' else '', order_value))

        return queryset

    def post(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            file = request.FILES['file']
            existing_media = Multimedia.has_file_already(file)
            if existing_media is None:
                media = Multimedia.create_and_upload(file, request.user, kwargs['vertical'])
            else:
                media = existing_media
            return Response(MultimediaSerializer(media).data)


class RetrieveUpdateDestroyMultimedia(generics.RetrieveUpdateDestroyAPIView):
    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
