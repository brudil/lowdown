from spectrum.base import BaseElement
from spectrum import fields
from spectrum import sections
from spectrum import blocks


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


SETS = {
    'all': (ArticleSubtype, VideoSubtype, )
}
