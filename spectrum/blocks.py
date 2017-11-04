from spectrum import fields
from spectrum import transformers
from spectrum.base import BaseElement
from spectrum import resources


class Block(BaseElement):
    pass


class HeadingBlock(Block):
    class Meta:
        name = 'heading'

    level = fields.ChoiceValueField(default_value=1, choices=(1, 2, 3, 4, 5, 6,), blank=False)
    text = fields.TextualContentField(default_transformer=transformers.InlinedownTextTransformer,
                                      limit_to=transformers.SETS['all'])


class PullQuoteBlock(Block):
    class Meta:
        name = 'pullquote'

    attribution = fields.TextualContentField(default_transformer=transformers.InlinedownTextTransformer,
                                      limit_to=transformers.SETS['all'])
    quote = fields.TextualContentField(default_transformer=transformers.InlinedownTextTransformer,
                                      limit_to=transformers.SETS['all'])


class ImageBlock(Block):
    class Meta:
        name = 'image'

    resource = fields.ElementField(limit_to=(resources.LowdownImageResource, ), default_element=resources.LowdownImageResource)
    alt = fields.TextualContentField(default_transformer=transformers.PlainTextTransformer)
    title = fields.TextualContentField(default_transformer=transformers.PlainTextTransformer)
    caption = fields.TextualContentField(default_transformer=transformers.InlinedownTextTransformer)
    source = fields.TextualContentField(default_transformer=transformers.InlinedownTextTransformer)
    sourceURL = fields.URLValueField(blank=True)
    container = fields.ChoiceValueField(default_value='CONTAINER', choices=('CONTENT', 'CONTAINER', 'BLEED', ), blank=False)


class CanvasBlock(Block):
    class Meta:
        name = 'canvas'

    resource = fields.ElementField(limit_to=(resources.LowdownInteractiveResource, ), default_element=resources.LowdownInteractiveResource)
    container = fields.ChoiceValueField(default_value='CONTAINER', choices=('CONTENT', 'CONTAINER', 'BLEED', ), blank=False)


class VideoBlock(Block):
    class Meta:
        name = 'video'

    reference = fields.ElementField(limit_to=(resources.OEmbedResource, ), default_element=resources.OEmbedResource)
    caption = fields.TextualContentField(default_transformer=transformers.InlinedownTextTransformer,
                                         limit_to=transformers.SETS['all'])


class TextBlock(Block):
    class Meta:
        name = 'text'

    text = fields.TextualContentField(default_transformer=transformers.MarkdownTextTransformer)


SETS = {
    'all': (HeadingBlock, ImageBlock, VideoBlock, TextBlock, PullQuoteBlock, CanvasBlock),
}
