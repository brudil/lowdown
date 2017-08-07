from spectrum.base import BaseElement
from spectrum import fields
from spectrum import sections
from spectrum import blocks
from spectrum import resources


class Subtype(BaseElement):
    class Meta:
        type = 'subtype'


class ArticleSubtype(Subtype):
    class Meta:
        name = 'article'

    stream = fields.FieldStreamField(fields.ElementField(limit_to=sections.SETS['all']))


class VideoSubtype(Subtype):
    class Meta:
        name = 'video'

    featured_video = fields.ElementField(limit_to=(blocks.VideoBlock, ), default_element=blocks.VideoBlock)
    stream = fields.FieldStreamField(fields.ElementField(limit_to=sections.SETS['all']))


class CanvasSubtype(Subtype):
    class Meta:
        name = 'canvas_subtype'

    resource = fields.ElementField(limit_to=(resources.LowdownInteractiveResource, ), default_element=resources.LowdownInteractiveResource)
    viewMode = fields.ChoiceValueField(default_value='CONTAINER', choices=('CONTENT', 'CONTAINER', 'CANVAS', ), blank=False)


SETS = {
    'all': (ArticleSubtype, VideoSubtype, CanvasSubtype)
}
