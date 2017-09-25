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

        def resolve_total_count(self, args, context, info):
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


class Author(DjangoObjectType):
    class Meta:
        model = author_models.Author

    all_content = DjangoConnectionField(lambda: Content)

    def resolve_all_content(self, args, context, info):
        queryset = content_models.Content.objects.filter(vertical=self.vertical, published_revision__isnull=False, published_revision__authors__in=[self])
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

    def resolve_all_content(self, args, context, info):
        queryset = content_models.Content.objects.filter(vertical=self.vertical, published_revision__isnull=False, published_revision__section=self)
        return queryset.order_by('-published_date')

    def resolve_all_topics(self, args, context, info):
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

    def resolve_object(self, args, context, info):
        return self.media_object

    def resolve_media_id(self, args, context, info):
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

    def resolve_release_number(self, args, context, info):
        latest = self.get_latest_public_release()
        if latest is None:
            return None

        return latest.revision_number



class ResourceMap(ObjectType):
    lowdownimages = graphene.List(MultimediaImage)
    lowdowninteractives = graphene.List(Interactive)

    def resolve_lowdownimages(self, args, context, info):
        try:
            return self.lowdownimage
        except AttributeError:
            return None

    def resolve_lowdowninteractives(self, args, context, info):
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

    def resolve_document(self, args, context, info):
        return self.spectrum_document

    def resolve_authors(self, args, context, info):
        return self.authors.all()

    def resolve_resources(self, args, context, info):
        return SimpleNamespace(**self.get_resources_map())

    def resolve_section(self, args, context, info):
        return self.section

    def resolve_series(self, args, context, info):
        return self.series

    def resolve_topics(self, args, context, info):
        return self.topics.all()


class ContentComment(DjangoObjectType):
    class Meta:
        model = content_models.ContentComment

    user = graphene.Field(User)

    def resolve_user(self, args, context, info):
        return self.user


class EditorialMetadata(DjangoObjectType):
    class Meta:
        model = content_models.ContentEditorialMetadata

    comments = graphene.List(ContentComment)

    def resolve_comments(self, args, context, info):
        return self.comments()


class Content(DjangoObjectType):
    class Meta:
        model = content_models.Content
        interfaces = (Node, )

    content = graphene.Field(ContentContent)
    editorial_metadata = graphene.Field(EditorialMetadata)
    content_id = graphene.Int()

    def resolve_content(self, args, context, info):
        return self.published_revision

    def resolve_content_id(self, args, context, info):
        return self.pk

    def resolve_editorial_metadata(self, args, context, info):
        return self.editorial_metadata

Content.Connection = connection_for_type(Content)


class ContentStats(graphene.ObjectType):
    total_stubs = graphene.Int()
    total_drafts = graphene.Int()
    total_final = graphene.Int()


class Vertical(ObjectType):
    all_content = DjangoConnectionField(Content, watching=graphene.Boolean(), form=graphene.Argument(Form, required=False), tone=graphene.Argument(Tone, required=False))
    content = graphene.Field(Content, content_id=graphene.Int())
    content_stats = graphene.Field(ContentStats)
    author = graphene.Field(Author, slug=graphene.String())
    section = graphene.Field(Section, slug=graphene.String())
    all_media = DjangoConnectionField(Multimedia)

    def resolve_all_content(self, args, context, info):
        queryset = content_models.Content.objects.filter(vertical=self.identifier)

        if args.get('watching') is not None and args.get('watching') is True:
            queryset = queryset.filter(editorial_metadata__contentwatcher__watcher=context.user,
                                       editorial_metadata__contentwatcher__silent=False)

        if args.get('form') is not None:
            queryset = queryset.filter(published_revision__form=args.get('form'))

        if args.get('tone') is not None:
            queryset = queryset.filter(published_revision__tone=args.get('tone'))

        return queryset.order_by('-published_date')

    def resolve_content_stats(self, args, context, info):
        return content_models.Content.get_stats_for_vertical(self.identifier)

    def resolve_content(self, args, context, info):
        return content_models.Content.objects.get(vertical=self.identifier, pk=args.get('content_id'))

    def resolve_author(self, args, context, info):
        return author_models.Author.objects.get(vertical=self.identifier, slug=args.get('slug'))

    def resolve_section(self, args, context, info):
        return section_models.Section.objects.get(vertical=self.identifier, slug=args.get('slug'))

    def resolve_all_media(self, args, context, info):
        return multimedia_models.Multimedia.objects.all().order_by('-created')


class Notification(DjangoObjectType):
    class Meta:
        model = notification_models.Notification

Notification.Connection = connection_for_type(Notification)


class Notifications(graphene.ObjectType):
    unread = graphene.Int()
    items = DjangoConnectionField(Notification.Connection)

    def resolve_unread(self, args, context, info):
        return notification_models.Notification.objects.filter(reciver=context.user)\
            .unread().count()

    def resolve_items(self, args, context, info):
        return notification_models.Notification.objects.filter(reciver=context.user)\
            .unread()


class ReleaseNote(DjangoObjectType):
    class Meta:
        model = releasenotes_models.ReleaseNote

ReleaseNote.Connection = connection_for_type(ReleaseNote)


class Query(graphene.ObjectType):
    # all_sections = graphene.List(ShowSlot, )
    # content = graphene.Field(Show, slug=graphene.String())
    vertical = graphene.Field(Vertical, identifier=graphene.String())
    media = graphene.Field(Multimedia, media_id=graphene.Int())
    notifications = graphene.Field(Notifications)
    release_notes = DjangoConnectionField(ReleaseNote.Connection)

    def resolve_vertical(self, args, context, info):
        identifier = args.get('identifier')
        vertical = verticals.MANAGER.get_by_identifier(identifier)

        if vertical is None:
            return None

        return vertical

    def resolve_media(self, args, context, info):
        return multimedia_models.Multimedia.objects.get(pk=args.get('media_id'))

    def resolve_notifications(self, args, context, info):
        return {}

    def resolve_release_notes(self, args, context, info):
        return releasenotes_models.ReleaseNote.objects.filter(deleted=False).order_by('-created')

        # def resolve_current_slate(self, args, context, info):
    #     return show_models.ShowsConfiguration.objects.get().current_slate
    #
    # def resolve_all_shows(self, args, context, info):
    #     return show_models.Show.objects.all()
    #
    # def resolve_all_members(self, args, context, info):
    #     return user_models.User.objects.all()
    #
    # def resolve_all_slates(self, args, context, info):
    #     return show_models.ScheduleSlate.objects.all()
    #
    # def resolve_all_episodes(self, args, context, info):
    #     return show_models.ShowEpisode.objects.all()
    #
    # def resolve_all_slots(self, args, context, info):
    #     return show_models.ShowSlot.objects.filter(slate=show_models.ShowsConfiguration.objects.get().current_slate)
    #
    # def resolve_viewer(self, args, context, info):
    #     return context.user if context.user.is_authenticated else None
    #

# todo: Query: Content -> Comments
# todo: Query: Content -> Watchers

# todo: Mutation: PostContentComment

# todo: Mutation: MarkNotificationsAsRead

# todo: Mutation: WatchContent
# todo: Mutation: UnwatchContent

# todo: Mutation: UnpublishContent
# todo: Mutation: ArchiveContent

# todo: Mutation: LockContent
# todo: Mutation: LockedStatusContent

# todo: Mutation: UploadMedia
# todo: Mutation: DeleteMedia
# todo: Mutation: EditMedia


class LockContent(graphene.Mutation):
    class Input:
        content_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, args, context, info):
        content_id = graphene.Int()
        try:
            content = content_models.Content.objects.get(pk=content_id)
        except content_models.Content.DoesNotExist:
            return LockContent(ok=False)

        if content is not None:
            content.lock_for(context.user)


class PostContentCommentInput(graphene.InputObjectType):
    revision_id = graphene.Int()
    comment = graphene.String()


class PostContentComment(graphene.Mutation):
    class Input:
        data = graphene.Argument(PostContentCommentInput)

    ok = graphene.Boolean()
    comment = graphene.Field(ContentComment)

    def mutate(self, args, context, info):
        data = args.get('data')

        try:
            content_revision = content_models.ContentRevision.objects.get(id=data['revision_id'])
            comment = content_revision.add_comment(context.user, data['comment'])
            return PostContentComment(ok=True, comment=comment)
        except content_models.Content.DoesNotExist:
            return PostContentComment(ok=False)


class Mutations(graphene.ObjectType):
    lock_content = LockContent.Field()
    post_content_comment = PostContentComment.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)
