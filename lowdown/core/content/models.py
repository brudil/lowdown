import uuid
from collections import namedtuple
from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models, IntegrityError
from django.db import transaction

from lowdown.core.interactives.models import Interactive
from lowdown.core.content import constants
from lowdown.core.verticals.fields import VerticalField
from lowdown.core.multimedia.models import Multimedia
from spectrum import resources
from spectrum.document import SpectrumDocument

# TODO: the resource resolve logic is rather poor and should be consolidated,
#       initially support was only build in to reference via primary key integers
#       but interactives use slugs, so there are a few messy if statements that should really be
#       moved to a config var or built in to spectrum

def resource_mapper(resource_name):
    map = {
        'lowdownimage': Multimedia.objects.prefetch_related('media_object'),
        'lowdowninteractive': Interactive.objects,
    }
    return map[resource_name]


ContentStats = namedtuple('ContentStats', ['total_drafts', 'total_final', 'total_stubs', 'total_published'])

def map_resources_by_name(resources_list):
    map_by_name = {}

    for resource in resources_list:
        resource_name = resource.Meta.name
        map_by_name.setdefault(resource_name, [])
        if resource_name == 'lowdowninteractive':
            map_by_name[resource_name].append(resource.slug)
        else:
            map_by_name[resource_name].append(resource.id)

    return map_by_name


def resource_resolver(resources_by_name):
    resources_map = {}

    for resource_name, ids in resources_by_name.items():
        queryset = resource_mapper(resource_name)
        if resource_name == 'lowdowninteractive':
            resources_map[resource_name] = queryset.filter(slug__in=ids)
        else:
            resources_map[resource_name] = queryset.filter(id__in=ids)

    return resources_map


class Content(models.Model):
    class Meta:
        db_table = 'content'

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    published_revision = models.ForeignKey('content.ContentRevision', null=True, blank=True, related_name='published')
    published_slug = models.SlugField(max_length=60, null=True, blank=True, unique=False)

    published_date = models.DateTimeField(null=True)
    published_updated_date = models.DateTimeField(null=True)
    vertical = VerticalField()

    deleted = models.BooleanField(default=False)

    def __str__(self):
        return 'Content #{}'.format(self.pk)

    @classmethod
    def get_stats_for_vertical(cls, vertical):
        total_draft = Content.objects.filter(
            vertical=vertical,
            editorial_metadata__current_revision__status=constants.STATUS_DRAFT,
            published_revision__isnull=True
        ).count()

        total_ready = Content.objects.filter(
            vertical=vertical,
            editorial_metadata__current_revision__status=constants.STATUS_FINAL,
            published_revision__isnull=True
        ).count()

        total_stubs = Content.objects.filter(
            vertical=vertical,
            editorial_metadata__current_revision__status=constants.STATUS_STUB,
            published_revision__isnull=True
        ).count()

        total_published = Content.objects.filter(
            vertical=vertical,
            published_revision__isnull=False
        ).count()

        return ContentStats(
            total_stubs=total_stubs,
            total_drafts=total_draft,
            total_final=total_ready,
            total_published=total_published,
        )

    @classmethod
    def from_revision(cls, revision_serializer, vertical, user):
        with transaction.atomic():
            content = cls()
            content.vertical = vertical
            content.save()

            revision_serializer.save(content=content, revision_number=1)
            revision = revision_serializer.instance
            revision.created_by = user
            revision.save()

            metadata = ContentEditorialMetadata()
            metadata.content = content
            metadata.current_revision = revision
            metadata.revision_count += 1

            metadata.save()

            metadata.add_watcher(user)

        return metadata


class ContentRevision(models.Model):
    class Meta:
        db_table = 'content_revision'

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    revision_number = models.PositiveIntegerField(null=False, default=0)
    created_by = models.ForeignKey('users.LowdownUser', null=True, related_name='revisions')

    content = models.ForeignKey('content.Content', db_index=True, null=False, related_name='revisions')
    series = models.ForeignKey('series.Series', null=True, blank=True,  default=None, related_name='content_revisions')
    section = models.ForeignKey('sections.Section', null=True, blank=True, default=None, related_name='content_revisions')
    topics = models.ManyToManyField('topics.Topic', blank=True, related_name='content_revisions')
    users = models.ManyToManyField('users.LowdownUser', blank=True, related_name='content_revisions')
    authors = models.ManyToManyField('authors.Author', blank=True, related_name='content_revisions')

    headline = models.TextField(null=False)
    short_headline = models.TextField(null=False, blank=True)
    byline_markup = models.TextField(null=False, blank=True)
    kicker = models.TextField(null=False, blank=True)
    standfirst = models.TextField(null=False, blank=True)

    poster_image = models.ForeignKey('multimedia.Multimedia', null=True, blank=True)

    status = models.SmallIntegerField(choices=constants.STATUS_CHOICES, null=False, default=constants.STATUS_DRAFT)

    slug = models.CharField(max_length=60, null=True, blank=True)
    tone = models.SmallIntegerField(choices=constants.TONE_CHOICES, null=False, db_index=True)
    form = models.SmallIntegerField(choices=constants.FORM_CHOICES, null=False, db_index=True)

    preview_key = models.UUIDField(default=uuid.uuid4, editable=False)

    spectrum_document = JSONField(blank=True)

    def get_issues_for_publication(self):
        if self.content is None:
            yield 'Content is empty'

        if self.authors.count() < 1:
            yield 'No authors'

        if self.headline == '':
            yield 'Empty headline'

    def get_spectrum_document(self):
        return SpectrumDocument.from_json(self.spectrum_document)

    def get_resources_for_document(self):
        document = self.get_spectrum_document()
        elements = document.get_elements()

        found_resources = [element for element in elements if (isinstance(element, resources.Resource) or isinstance(element, resources.LowdownInteractiveResource))]

        return map_resources_by_name(found_resources)

    def get_resources_map(self):
        resources_from_document = self.get_resources_for_document()

        return resource_resolver(resources_from_document)

    def can_publish(self):
        return self.status == 9

    def change_status(self, status):
        if status in [1, 5, 9]:
            self.status = status
            self.save()
            return True

        return False

    def publish(self):
        if self.status != 9:
            raise ValueError('only final revisions can be published')

        with transaction.atomic():
            content = self.content
            content.published_revision = self
            content.published_slug = self.slug
            content.published_updated_date = datetime.now()

            if content.published_date is None:
                content.published_date = datetime.now()

            content.save()

            editorial = self.content.editorial_metadata

            editorial.save()

        return content

    def add_comment(self, user, comment):
        comment = ContentComment.objects.create(user=user, comment=comment, revision=self)
        return comment

    def __str__(self):
        return self.headline


class ContentComment(models.Model):
    revision = models.ForeignKey(ContentRevision)
    user = models.ForeignKey('users.LowdownUser', related_name='content_comments')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


class ContentEditorialMetadata(models.Model):
    class Meta:
        db_table = 'content_editorial_metadata'

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    content = models.OneToOneField('content.Content', related_name='editorial_metadata')
    current_revision = models.OneToOneField('content.ContentRevision')

    locked_at = models.DateTimeField(null=True, blank=True, default=None)

    revision_count = models.IntegerField(default=0, null=False)

    watchers = models.ManyToManyField(to='users.LowdownUser', through='content.ContentWatcher')

    def __str__(self):
        return 'Content Editorial Metadata #{}'.format(self.content.pk)

    def comments(self):
        return ContentComment.objects.filter(revision__content=self.content, deleted=False)\
            .order_by('created')

    def lock_writes(self, user):
        # TODO: lock via redis
        # redis.setnx(self.content.pk, user) for 30 seconds
        return True # return if successful

    def is_locked(self):
        pass
    # TODO: see if locked
    # redis.get(self.content.pk)
    #return (True, get_user)

    def add_watcher(self, user):
        try:
            ContentWatcher.objects.get(content_editorial_metadata=self, watcher=user)
        except ContentWatcher.DoesNotExist:
            ContentWatcher.objects.create(watcher=user, content_editorial_metadata=self)

    def watchers(self):
        return ContentWatcher.objects.filter(content_editorial_metadata=self)

    @property
    def published(self):
        return self.content.published_date is not None


class ContentWatcher(models.Model):
    content_editorial_metadata = models.ForeignKey(ContentEditorialMetadata)
    watcher = models.ForeignKey('users.LowdownUser', related_name='watching_content')
    silent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('content_editorial_metadata', 'watcher')
