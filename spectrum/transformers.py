from typing import Any

from spectrum.base import BaseElement


class Transformer(BaseElement):
    pass


class TextTransformer(Transformer):
    pass


class InlinedownTextTransformer(TextTransformer):
    class Meta:
        name = 'inline'


class MarkdownTextTransformer(TextTransformer):
    class Meta:
        name = 'markdown'


class PlainTextTransformer(TextTransformer):
    class Meta:
        name = 'plain'


SETS = {
    'all': (InlinedownTextTransformer, MarkdownTextTransformer, PlainTextTransformer)
}
