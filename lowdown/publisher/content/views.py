import django_filters
from django.shortcuts import get_object_or_404
from rest_framework import permissions

from lowdown.core.content.models import Content
from lowdown.publisher.content.serializers import ContentListSerializer, ContentDetailSerializer
from lowdown.core.topics.models import Topic
from lowdown.core.users.models import LowdownUser
from rest_framework import filters
from rest_framework import generics


class ContentListFilter(filters.FilterSet):
    status = django_filters.NumberFilter(name='status')
    form = django_filters.NumberFilter(name='current_revision__form')
    tone = django_filters.NumberFilter(name='current_revision__tone')
    topics = django_filters.ModelMultipleChoiceFilter(name='current_revision__topics', queryset=Topic.objects.all())
    series = django_filters.ModelChoiceFilter(name='current_revision__series', queryset=LowdownUser.objects.all())

    class Meta:
        model = Content
        exclude = ()


# LIST /content
# DETAIL /content/{id}/revision


class ListContent(generics.ListAPIView):
    serializer_class = ContentListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = ContentListFilter
    search_fields = ('published_revision__headline',)

    def get_queryset(self):
        return Content.objects.filter(vertical=self.kwargs['vertical'], published_revision__isnull=False) \
                .order_by('-published_date') \
            .select_related(
            'published_revision',
            'published_revision__poster_image',
            'published_revision__section',
            'published_revision__series',
        ).prefetch_related(
            'published_revision__authors',
            'published_revision__topics',
            'published_revision__poster_image__media_object',
        )


class RetrieveContent(generics.RetrieveAPIView):
    serializer_class = ContentDetailSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        content = get_object_or_404(Content.objects.select_related(
            'published_revision',
            'published_revision__poster_image',
            'published_revision__section',
            'published_revision__series',
        ).prefetch_related(
            'published_revision__poster_image__media_object',
            'published_revision__authors',
            'published_revision__topics',
        ), pk=self.kwargs['pk'], vertical=self.kwargs['vertical'])
        return content.published_revision
