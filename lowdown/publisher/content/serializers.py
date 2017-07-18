from lowdown.core.content.models import Content, ContentEditorialMetadata, ContentRevision
from lowdown.manage.users.serializers import UserSerializer
from lowdown.publisher.multimedia.serializers import MultimediaImageSerializer
from rest_framework import serializers

from lowdown.publisher.sections.serializers import MinimalSectionSerializer


class ContentListSerializer(serializers.ModelSerializer):
    published = serializers.DateTimeField(source='published_date')
    updated = serializers.DateTimeField(source='published_updated_date')
    authors = UserSerializer(read_only=True, many=True, source='published_revision.authors')
    poster_image = MultimediaImageSerializer(source='published_revision.poster_image')
    section = MinimalSectionSerializer(source='published_revision.section')
    headline = serializers.CharField(source='published_revision.headline')
    standfirst = serializers.CharField(source='published_revision.standfirst')
    short_headline = serializers.CharField(source='published_revision.short_headline')
    kicker = serializers.CharField(source='published_revision.kicker')
    tone = serializers.IntegerField(source='published_revision.tone')
    form = serializers.IntegerField(source='published_revision.form')
    slug = serializers.SlugField(source='published_slug')

    class Meta:
        model = Content
        fields = (
            'id',
            'published',
            'updated',
            'poster_image',
            'section',
            'authors',
            'headline',
            'short_headline',
            'poster_image',
            'short_headline',
            'kicker',
            'standfirst',
            'slug',
            'tone',
            'form',
        )


class ContentDetailSerializer(serializers.ModelSerializer):
    authors = UserSerializer(read_only=True, many=True)
    poster_image = MultimediaImageSerializer()
    id = serializers.IntegerField(source='content.id')
    published = serializers.DateTimeField(source='content.published_date')
    updated = serializers.DateTimeField(source='content.published_updated_date')
    resources = serializers.SerializerMethodField()
    section = MinimalSectionSerializer()

    class Meta:
        model = ContentRevision
        fields = (
            'id',
            'published',
            'updated',
            'poster_image',
            'authors',
            'headline',
            'short_headline',
            'poster_image',
            'short_headline',
            'kicker',
            'standfirst',
            'spectrum_document',
            'slug',
            'tone',
            'form',
            'section',
            'resources',
        )

    def get_resources(self, obj):
        resources_serializers = {
            'lowdownimage': MultimediaImageSerializer,
        }
        resources = {}

        for resource_name, queryset in obj.get_resources_map().items():
            resources[resource_name] = resources_serializers[resource_name](queryset, many=True).data

        return resources



