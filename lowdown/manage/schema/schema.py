from graphene import ObjectType, Node
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType, DjangoConnectionField
import graphene
from types import SimpleNamespace
from lowdown.core.content import models as content_models
from lowdown.core.content import constants
from lowdown.core.multimedia import models as multimedia_models
from lowdown.core.users import models as user_models
from lowdown.core.series import models as series_models
from lowdown.core.topics import models as topic_models
from lowdown.core.sections import models as section_models
from lowdown.core.authors import models as author_models
from lowdown.core.verticals import structure as verticals
from lowdown.core.interactives import models as interactives_models
from lowdown.manage.notifications import models as notification_models
from lowdown.manage.releasenotes import models as releasenotes_models


def connection_for_type(_type):
    class Connection(graphene.Connection):
        total_count = graphene.Int()

        class Meta:
            name = _type._meta.name + 'Connection'
            node = _type

        def resolve_total_count(self, info):
            return self.length

    return Connection


Form = graphene.Enum('Form', [
    ('ARTICLE', constants.FORM_ARTICLE),
    ('VIDEO', constants.FORM_VIDEO),
    ('INTERACTIVE', constants.FORM_INTERACTIVE),
    ('GALLERY', constants.FORM_GALLERY),
])

Tone = graphene.Enum('Tone', [
    ('CONTENT', constants.TONE_CONTENT),
    ('REVIEW', constants.TONE_REVIEW),
    ('VIEWPOINT', constants.TONE_VIEWPOINT),
    ('STORYTELLING', constants.TONE_STORYTELLING),
    ('INTERACTIVE', constants.TONE_INTERACTIVE),
    ('GUIDE', constants.TONE_GUIDE),
    ('NEWS', constants.TONE_NEWS),
])


class User(DjangoObjectType):
    class Meta:
        model = user_models.LowdownUser

    user_id = graphene.Int()

    def resolve_user_id(self, info):
        return self.pk


class Author(DjangoObjectType):
    class Meta:
        model = author_models.Author

    all_content = DjangoConnectionField(lambda: Content)

    def resolve_all_content(self, info):
        queryset = content_models.Content.objects.filter(
            vertical=self.vertical,
            published_revision__isnull=False,
            published_revision__authors__in=[self]
        )
        return queryset.order_by('-published_date')


class Topic(DjangoObjectType):
    class Meta:
        model = topic_models.Topic
        interfaces = (Node, )
        only_fields = (
            'id',
            'title',
            'slug',
            'section',
        )


class Section(DjangoObjectType):
    class Meta:
        model = section_models.Section
        only_fields = (
            'id',
            'title',
            'slug',
            'vertical',
        )

    all_content = DjangoConnectionField(lambda: Content)
    all_topics = DjangoConnectionField(Topic)

    def resolve_all_content(self, info):
        queryset = content_models.Content.objects.filter(
            vertical=self.vertical,
            published_revision__isnull=False,
            published_revision__section=self
        )
        return queryset.order_by('-published_date')

    def resolve_all_topics(self, info):
        return self.topics.all()


class Series(DjangoObjectType):
    class Meta:
        model = series_models.Series
        only_fields = (
            'id',
            'title',
            'slug',
        )


class Multimedia(DjangoObjectType):
    class Meta:
        model = multimedia_models.Multimedia
        interfaces = (graphene.relay.Node, )
        exclude_fields = ('tags', )

    object = graphene.Field(lambda: MediaTypes)
    media_id = graphene.Int()

    def resolve_object(self, info):
        return self.media_object

    def resolve_media_id(self, info):
        return self.pk


class MultimediaImage(DjangoObjectType):
    class Meta:
        model = multimedia_models.MultimediaImage


class MediaTypes(graphene.Union):
    class Meta:
        types = (MultimediaImage, )

# def get_embedded_image(model, name):
#     if getattr(model, name) is None:
#         return None
#
#     return EmbeddedImage(
#         resource=getattr(model, name),
#         width=getattr(model, '{}_width'.format(name)),
#         height=getattr(model, '{}_height'.format(name)),
#     )


class Interactive(DjangoObjectType):
    class Meta:
        model = interactives_models.Interactive
        only_fields = ('slug', )

    release_number = graphene.Int()

    def resolve_release_number(self, info):
        latest = self.get_latest_public_release()
        if latest is None:
            return None

        return latest.revision_number


class ResourceMap(ObjectType):
    lowdownimages = graphene.List(MultimediaImage)
    lowdowninteractives = graphene.List(Interactive)

    def resolve_lowdownimages(self, info):
        try:
            return self.lowdownimage
        except AttributeError:
            return None

    def resolve_lowdowninteractives(self, info):
        try:
            return self.lowdowninteractive
        except AttributeError:
            return None


class ContentContent(DjangoObjectType):
    class Meta:
        model = content_models.ContentRevision

    document = GenericScalar()
    resources = graphene.Field(ResourceMap)
    poster_image = graphene.Field(MultimediaImage)
    authors = graphene.List(Author, )
    section = graphene.Field(Section)
    series = graphene.Field(Series)
    topics = graphene.List(Topic, )
    form = graphene.Field(Form)
    tone = graphene.Field(Tone)

    def resolve_document(self, info):
        return self.get_spectrum_document_as_dict()

    def resolve_authors(self, info):
        return self.authors.all()

    def resolve_resources(self, info):
        return SimpleNamespace(**self.get_resources_map())

    def resolve_section(self, info):
        return self.section

    def resolve_series(self, info):
        return self.series

    def resolve_topics(self, info):
        return self.topics.all()


class ContentComment(DjangoObjectType):
    class Meta:
        model = content_models.ContentComment

    user = graphene.Field(User)

    def resolve_user(self, info):
        return self.user


class ContentWatcher(DjangoObjectType):
    class Meta:
        model = content_models.ContentWatcher

    user = graphene.Field(User)

    def resolve_user(self, info):
        return self.watcher


class EditorialMetadata(DjangoObjectType):
    class Meta:
        model = content_models.ContentEditorialMetadata

    comments = graphene.List(ContentComment)
    watchers = graphene.List(ContentWatcher)

    def resolve_comments(self, info):
        return self.comments()

    def resolve_watchers(self, info):
        return self.get_watchers()


class Content(DjangoObjectType):
    class Meta:
        model = content_models.Content
        interfaces = (Node, )

    content = graphene.Field(ContentContent)
    editorial_metadata = graphene.Field(EditorialMetadata)
    content_id = graphene.Int()

    def resolve_content(self, info):
        return self.published_revision

    def resolve_content_id(self, info):
        return self.pk

    def resolve_editorial_metadata(self, info):
        return self.editorial_metadata

Content.Connection = connection_for_type(Content)


class ContentStats(graphene.ObjectType):
    total_stubs = graphene.Int()
    total_drafts = graphene.Int()
    total_final = graphene.Int()
    total_published = graphene.Int()


class Vertical(ObjectType):
    all_content = DjangoConnectionField(
        Content,
        watching=graphene.Boolean(),
        published=graphene.Boolean(),
        form=graphene.Argument(Form, required=False),
        tone=graphene.Argument(Tone, required=False)
    )
    content = graphene.Field(Content, content_id=graphene.Int())
    last_published = graphene.Field(Content, content_id=graphene.Int())
    content_stats = graphene.Field(ContentStats)
    author = graphene.Field(Author, slug=graphene.String())
    section = graphene.Field(Section, slug=graphene.String())
    all_media = DjangoConnectionField(Multimedia)

    def resolve_all_content(self, info, **kwargs):
        queryset = content_models.Content.objects.filter(vertical=self.identifier)
        watching = kwargs.get('watching') or None
        published = kwargs.get('published', None)
        form = kwargs.get('form') or None
        tone = kwargs.get('tone') or None

        if watching is not None and watching is True:
            queryset = queryset.filter(
                editorial_metadata__contentwatcher__watcher=info.context.user,
                editorial_metadata__contentwatcher__silent=False
            )

        if form is not None:
            queryset = queryset.filter(published_revision__form=form)

        if tone is not None:
            queryset = queryset.filter(published_revision__tone=tone)

        if published is not None:
            queryset = queryset.filter(published_revision__isnull=(True if published is False else False))

        return queryset.order_by('-editorial_metadata__updated')

    def resolve_content_stats(self, info):
        return content_models.Content.get_stats_for_vertical(self.identifier)

    def resolve_content(self, info, content_id=None):
        return content_models.Content.objects.get(vertical=self.identifier, pk=content_id)

    def resolve_last_published(self, info):
        return content_models.Content.objects\
            .filter(vertical=self.identifier, published_revision__isnull=False)\
            .order_by('published_date').last()

    def resolve_author(self, info, slug=None):
        return author_models.Author.objects.get(vertical=self.identifier, slug=slug)

    def resolve_section(self, info, slug=None):
        return section_models.Section.objects.get(vertical=self.identifier, slug=slug)

    def resolve_all_media(self, info,  **kwargs):
        return multimedia_models.Multimedia.objects\
            .filter(vertical=self.identifier, deleted=False)\
            .order_by('-created')


class Notification(DjangoObjectType):
    class Meta:
        model = notification_models.Notification
        interfaces = (Node, )

# Notification.Connection = connection_for_type(Notification)


class Notifications(graphene.ObjectType):
    unread = graphene.Int()
    items = DjangoConnectionField(Notification)

    def resolve_unread(self, info):
        return notification_models.Notification.objects.filter(reciver=info.context.user)\
            .unread().count()

    def resolve_items(self, info):
        return notification_models.Notification.objects.filter(reciver=info.context.user)\
            .unread()


class ReleaseNote(DjangoObjectType):
    class Meta:
        model = releasenotes_models.ReleaseNote
        interfaces = (Node, )

# ReleaseNote.Connection = connection_for_type(ReleaseNote)


class Query(graphene.ObjectType):
    # all_sections = graphene.List(ShowSlot, )
    # content = graphene.Field(Show, slug=graphene.String())
    vertical = graphene.Field(Vertical, identifier=graphene.String())
    media = graphene.Field(Multimedia, media_id=graphene.Int())
    notifications = graphene.Field(Notifications)
    release_notes = DjangoConnectionField(ReleaseNote)
    content = graphene.Field(Content, content_id=graphene.Int())

    def resolve_vertical(self, info, identifier=None):
        vertical = verticals.MANAGER.get_by_identifier(identifier)

        if vertical is None:
            return None

        return vertical

    def resolve_content(self, info, content_id=None):
        return content_models.Content.objects.get(pk=content_id)

    def resolve_media(self, info, media_id=None):
        return multimedia_models.Multimedia.objects.get(pk=media_id)

    def resolve_notifications(self, info):
        return {}

    def resolve_release_notes(self, info, **kwargs):
        return releasenotes_models.ReleaseNote.objects.filter(deleted=False).order_by('-created')

# todo: Mutation: MarkNotificationsAsRead

# todo: Mutation: UnwatchContent

# todo: Mutation: UnpublishContent
# todo: Mutation: ArchiveContent

# todo: Mutation: LockContent
# todo: Mutation: LockedStatusContent

# todo: Mutation: UploadMedia
# todo: Mutation: DeleteMedia


class LockContent(graphene.Mutation):
    class Arguments:
        content_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, content_id=None):
        content_id = graphene.Int()
        try:
            content = content_models.Content.objects.get(pk=content_id)
        except content_models.Content.DoesNotExist:
            return LockContent(ok=False)

        if content is not None:
            content.lock_for(info.context.user)


class PostContentCommentInput(graphene.InputObjectType):
    revision_id = graphene.Int()
    comment = graphene.String()


class PostContentComment(graphene.Mutation):
    class Arguments:
        data = graphene.Argument(PostContentCommentInput)

    ok = graphene.Boolean()
    comment = graphene.Field(ContentComment)

    def mutate(self, info, data=None):
        try:
            content_revision = content_models.ContentRevision.objects.get(id=data['revision_id'])
            comment = content_revision.add_comment(info.context.user, data['comment'])
            return PostContentComment(ok=True, comment=comment)
        except content_models.Content.DoesNotExist:
            return PostContentComment(ok=False)


class WatchContent(graphene.Mutation):
    class Arguments:
        content_id = graphene.Int()

    ok = graphene.Boolean()
    editorial_metadata = graphene.Field(EditorialMetadata)

    def mutate(self, info, content_id=None):
        try:
            content_editorial = content_models.ContentEditorialMetadata.objects\
                .get(content=content_id)
            content_editorial.add_watcher(info.context.user)
            return WatchContent(ok=True, editorial_metadata=content_editorial)
        except content_models.Content.DoesNotExist:
            return WatchContent(ok=False)


class EditMedia(graphene.Mutation):
    class Arguments:
        media_id = graphene.Int()
        credit_title = graphene.String()
        credit_url = graphene.String()

    ok = graphene.Boolean()
    media = graphene.Field(Multimedia)

    def mutate(self, info, media_id=None, credit_title=None, credit_url=None):
        try:
            media = multimedia_models.Multimedia.objects\
                .get(pk=media_id)

            media.credit_title = credit_title
            media.credit_url = credit_url

            media.save()

            return EditMedia(ok=True, media=media)
        except content_models.Content.DoesNotExist:
            return EditMedia(ok=False)


class DeleteMedia(graphene.Mutation):
    class Arguments:
        media_id = graphene.Int()

    ok = graphene.Boolean()
    media = graphene.Field(Multimedia)

    def mutate(self, info, media_id=None):
        try:
            media = multimedia_models.Multimedia.objects\
                .get(pk=media_id)

            media.deleted = True

            media.save()

            return DeleteMedia(ok=True, media=media)
        except content_models.Content.DoesNotExist:
            return DeleteMedia(ok=False)


class UndeleteMedia(graphene.Mutation):
    class Arguments:
        media_id = graphene.Int()

    ok = graphene.Boolean()
    media = graphene.Field(Multimedia)

    def mutate(self, info, media_id=None):
        try:
            media = multimedia_models.Multimedia.objects\
                .get(pk=media_id)

            media.deleted = False

            media.save()

            return DeleteMedia(ok=True, media=media)
        except content_models.Content.DoesNotExist:
            return DeleteMedia(ok=False)


class Mutations(graphene.ObjectType):
    lock_content = LockContent.Field()
    post_content_comment = PostContentComment.Field()
    watch_content = WatchContent.Field()
    edit_media = EditMedia.Field()
    delete_media = DeleteMedia.Field()
    undelete_media = UndeleteMedia.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)
