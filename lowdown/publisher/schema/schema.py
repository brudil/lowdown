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


class Author(DjangoObjectType):
    class Meta:
        model = author_models.Author


class Topic(DjangoObjectType):
    class Meta:
        model = topic_models.Topic
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
        only_fields = ('id', 'resource_name', )

    width = graphene.Int()
    height = graphene.Int()

    def resolve_width(self, args, context, info):
        return self.media_object.width

    def resolve_height(self, args, context, info):
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


class ResourceMap(ObjectType):
    lowdownimages = graphene.List(MultimediaImage)

    def resolve_lowdownimages(self, args, context, info):
        try:
            return self.lowdownimage
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
    content_id = graphene.Int()

    def resolve_content(self, args, context, info):
        return self.published_revision

    def resolve_content_id(self, args, context, info):
        return self.pk

Content.Connection = connection_for_type(Content)


class Vertical(ObjectType):
    all_content = DjangoConnectionField(Content, )
    content = graphene.Field(Content, content_id=graphene.Int())

    def resolve_all_content(self, args, context, info):
        return content_models.Content.objects.filter(vertical=self.identifier, published_revision__isnull=False).order_by('-published_date')

    def resolve_content(self, args, context, info):
        return content_models.Content.objects.get(vertical=self.identifier, pk=args.get('content_id'), published_revision__isnull=False)


class Query(graphene.ObjectType):
    # all_sections = graphene.List(ShowSlot, )
    # content = graphene.Field(Show, slug=graphene.String())
    vertical = graphene.Field(Vertical, identifier=graphene.String())

    def resolve_vertical(self, args, context, info):
        identifier = args.get('identifier')
        vertical = verticals.MANAGER.get_by_identifier(identifier)

        if vertical is None:
            return None

        return vertical

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
