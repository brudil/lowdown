from django.db import transaction
from lowdown.core.content.models import Content, ContentRevision, ContentEditorialMetadata
from lowdown.core.authors.models import Author
from lowdown.manage.content.serializers import ContentEditorialMetadataSerializer, ContentRevisionSerializer, \
    ContentRevisionLocalSerializer
from lowdown.core.topics.models import Topic
from lowdown.core.users.models import LowdownUser
from django.shortcuts import get_object_or_404
import django_filters
from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView


class ContentListFilter(django_filters.rest_framework.FilterSet):
    status = django_filters.NumberFilter(name='current_revision__status')
    form = django_filters.NumberFilter(name='current_revision__form')
    tone = django_filters.NumberFilter(name='current_revision__tone')
    topics = django_filters.ModelMultipleChoiceFilter(name='current_revision__topics', queryset=Topic.objects.all())
    series = django_filters.ModelChoiceFilter(name='current_revision__series', queryset=LowdownUser.objects.all())
    authors = django_filters.ModelChoiceFilter(name='current_revision__authors', queryset=Author.objects.all())

    class Meta:
        model = ContentEditorialMetadata
        exclude = ()


# LIST /content
# DETAIL /content/{id}/revision


class ListCreateContent(generics.ListAPIView):
    serializer_class = ContentEditorialMetadataSerializer
    filter_class = ContentListFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('current_revision__headline', )

    def get_queryset(self):
        queryset = ContentEditorialMetadata.objects.select_related(
            'content',
            'content__published_revision',
            'current_revision',
            'current_revision__poster_image',
            'current_revision__series',
            'current_revision__section',
        ).prefetch_related(
            'current_revision__authors',
            'current_revision__topics',
        )

        vertical = self.kwargs['vertical']
        queryset = queryset.filter(content__vertical=vertical)

        if 'state' in self.request.query_params and self.request.query_params['state'] in ['internal', 'live']:
            queryset = queryset.filter(content__published_revision__isnull=self.request.query_params['state'] == 'internal')

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
        serializer = ContentRevisionLocalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        metadata = Content.from_revision(serializer, kwargs['vertical'], self.request.user)

        return Response(ContentRevisionSerializer(instance=metadata.current_revision).data)


class PublishContentRevision(APIView):
    def post(self, request, pk):
        revision = get_object_or_404(ContentRevision, pk=self.kwargs['pk'])

        revision.publish()

        editorial_metadata = revision.content.editorial_metadata
        return Response(ContentEditorialMetadataSerializer(instance=editorial_metadata).data)


class StatusContentRevision(APIView):
    def post(self, request, pk):
        revision = get_object_or_404(ContentRevision, pk=self.kwargs['pk'])
        print(self.request.data)
        revision.change_status(self.request.data['status'])

        return Response({'okay': True})


class RetrieveEditorialMetadata(generics.RetrieveAPIView):
    serializer_class = ContentEditorialMetadataSerializer
    queryset = ContentEditorialMetadata.objects.all()

    def get_object(self):
        print(self.kwargs)
        metadata = get_object_or_404(ContentEditorialMetadata, content=self.kwargs['pk'])
        return metadata


class RetrieveCurrentRevision(generics.RetrieveAPIView):
    serializer_class = ContentRevisionSerializer

    def get_object(self):
        metadata = get_object_or_404(ContentEditorialMetadata, content=self.kwargs['pk'])
        print(metadata.current_revision.get_resources_for_document())
        return metadata.current_revision


class CreateRevision(generics.CreateAPIView):
    serializer_class = ContentRevisionSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()
            new_revision = serializer.instance
            editorial = new_revision.content.editorial_metadata
            editorial.current_revision = new_revision
            editorial.revision_count += 1

            editorial.save()
            editorial.add_watcher(self.request.user)
            new_revision.created_by = self.request.user
            new_revision.revision_number = editorial.revision_count
            new_revision.save()
