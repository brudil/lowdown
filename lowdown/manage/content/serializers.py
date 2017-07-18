from lowdown.core.content.models import Content, ContentEditorialMetadata, ContentRevision
from lowdown.core.sections.models import Section
from lowdown.core.series.models import Series
from lowdown.core.topics.models import Topic
from lowdown.manage.series.serializers import SeriesSerializer
from lowdown.manage.sections.serializers import SectionSerializer
from lowdown.manage.topics.serializers import TopicSerializer
from lowdown.manage.users.serializers import UserSerializer
from lowdown.core.users.models import LowdownUser
from rest_framework import serializers


class ContentRevisionSerializer(serializers.ModelSerializer):
    section_nest = SectionSerializer(read_only=True, source='section')
    section = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Section.objects.all())
    series_nest = SeriesSerializer(read_only=True, source='series')
    series = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Series.objects.all())
    topics_nest = TopicSerializer(read_only=True, many=True, source='topics')
    topics = serializers.PrimaryKeyRelatedField(many=True, queryset=Topic.objects.all())
    authors_nest = UserSerializer(read_only=True, many=True, source='authors')
    authors = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=LowdownUser.objects.all())

    class Meta:
        model = ContentRevision
        fields = (
            'id',
            'created',
            'updated',
            'revision_number',

            'content',
            'series_nest',
            'series',
            'section_nest',
            'section',
            'topics_nest',
            'topics',
            'authors',
            'authors_nest',

            'poster_image',

            'headline',
            'short_headline',
            'byline_markup',
            'kicker',
            'standfirst',
            'slug',
            'tone',
            'form',
            'status',

            'spectrum_document'
        )


class ContentRevisionLocalSerializer(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Section.objects.all())
    series = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Series.objects.all())
    topics = serializers.PrimaryKeyRelatedField(many=True, queryset=Topic.objects.all())
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=LowdownUser.objects.all())

    class Meta:
        model = ContentRevision
        fields = (
            'series',
            'section',
            'topics',
            'authors',

            'poster_image',

            'headline',
            'short_headline',
            'byline_markup',
            'kicker',
            'standfirst',
            'slug',
            'tone',
            'form',
            'status',

            'spectrum_document'
        )


class ContentRevisionListSerializer(serializers.ModelSerializer):
    authors = UserSerializer(read_only=True, many=True)

    class Meta:
        model = ContentRevision
        fields = (
            'created',
            'updated',

            'series',
            'topics',
            'authors',

            'revision_number',

            'headline',
            'tone',
            'form',
            'status',
        )


class ContentEditorialMetadataSerializer(serializers.ModelSerializer):
    current_revision = ContentRevisionListSerializer(read_only=True)
    published_revision = ContentRevisionListSerializer(read_only=True, source='content.published_revision')
    published_date = serializers.DateTimeField(read_only=True, source='content.published_date')
    published_updated_date = serializers.DateTimeField(read_only=True, source='content.published_updated_date')

    class Meta:
        model = ContentEditorialMetadata
        fields = (
            'id',
            'created',
            'updated',

            'locked_at',
            'revision_count',

            'current_revision',
            'content',
            'published_revision',

            'published',
            'published_date',
            'published_updated_date',
        )
