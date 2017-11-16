from graphene import ObjectType, Node
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType, DjangoConnectionField
import graphene
from types import SimpleNamespace
from lowdown.core.content import models as content_models
from lowdown.core.content import constants
from lowdown.core.multimedia import models as multimedia_models
from lowdown.core.series import models as series_models
from lowdown.core.topics import models as topic_models
from lowdown.core.sections import models as section_models
from lowdown.core.authors import models as author_models
from lowdown.core.verticals import structure as verticals
from lowdown.core.interactives import models as interactives_models


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


class Author(DjangoObjectType):
    class Meta:
        model = author_models.Author

    all_content = DjangoConnectionField(lambda: Content)

    def resolve_all_content(self, info):
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

    def resolve_all_content(self, info):
        queryset = content_models.Content.objects.filter(vertical=self.vertical, published_revision__isnull=False, published_revision__section=self)
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
        only_fields = ('id', 'resource_name', )


class MultimediaImage(DjangoObjectType):
    class Meta:
        model = multimedia_models.Multimedia
        only_fields = ('id', 'resource_name', 'credit_title', 'credit_url')

    width = graphene.Int()
    height = graphene.Int()

    def resolve_width(self, info):
        return self.media_object.width

    def resolve_height(self, info):
        return self.media_object.height
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


class Content(DjangoObjectType):
    class Meta:
        model = content_models.Content
        interfaces = (Node, )
        only_fields = (
            'id',
            'content',
            'content_id',
            'published_date',
            'published_updated_date',
            'vertical'
        )

    content = graphene.Field(ContentContent)
    related_content = graphene.List(lambda: Content)
    content_id = graphene.Int()

    def resolve_content(self, info):
        return self.published_revision

    def resolve_content_id(self, info):
        return self.pk

    def resolve_related_content(self, info):
        return self.related_content()[:6]
Content.Connection = connection_for_type(Content)


class Vertical(ObjectType):
    all_content = DjangoConnectionField(Content, form=graphene.Argument(Form, required=False), tone=graphene.Argument(Tone, required=False))
    content = graphene.Field(Content, content_id=graphene.Int())
    author = graphene.Field(Author, slug=graphene.String())
    section = graphene.Field(Section, slug=graphene.String())

    def resolve_all_content(self, info, form=None, tone=None):
        queryset = content_models.Content.objects.filter(vertical=self.identifier, published_revision__isnull=False)

        if form is not None:
            queryset = queryset.filter(published_revision__form=form)

        if tone is not None:
            queryset = queryset.filter(published_revision__tone=tone)

        return queryset.order_by('-published_date')

    def resolve_content(self, info, content_id=None):
        return content_models.Content.objects.get(vertical=self.identifier, pk=content_id, published_revision__isnull=False)

    def resolve_author(self, info, slug=None):
        return author_models.Author.objects.get(vertical=self.identifier, slug=slug)

    def resolve_section(self, info, slug=None):
        return section_models.Section.objects.get(vertical=self.identifier, slug=slug)


class Query(graphene.ObjectType):
    # all_sections = graphene.List(ShowSlot, )
    # content = graphene.Field(Show, slug=graphene.String())
    vertical = graphene.Field(Vertical, identifier=graphene.String())
    preview_content = graphene.Field(ContentContent, revision_id=graphene.Int(), preview_key=graphene.String())
    image = graphene.Field(MultimediaImage, media_id=graphene.Int())

    def resolve_vertical(self, info, identifier=None):
        vertical = verticals.MANAGER.get_by_identifier(identifier)

        if vertical is None:
            return None

        return vertical

    def resolve_preview_content(self, info, revision_id=None, preview_key=None):
        return content_models.ContentRevision.objects.get(pk=revision_id, preview_key=preview_key)

    def resolve_image(self, info, media_id=None):
        return multimedia_models.Multimedia.objects.get(pk=media_id)

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

schema = graphene.Schema(query=Query)
