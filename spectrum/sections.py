from spectrum import fields
from spectrum import base
from spectrum import blocks


class Section(base.BaseElement):
    pass


class FreeformSection(Section):
    class Meta:
        name = 'freeform'

    def __init__(self, stream=None):
        super().__init__()
        if stream is not None:
            l = list()
            l.extend(stream)
            self.stream = l

    stream = fields.FieldStreamField(fields.ElementField(limit_to=blocks.SETS['all']))


class ListSectionItem(base.BaseElement):
    class Meta:
        name = 'listitem'

    title = fields.ElementField(default_element=blocks.HeadingBlock, limit_to=(blocks.HeadingBlock, ))
    stream = fields.FieldStreamField(fields.ElementField(limit_to=blocks.SETS['all']))


class ListSection(Section):
    class Meta:
        name = 'list'

    stream = fields.FieldStreamField(fields.ElementField(default_element=ListSectionItem, limit_to=(ListSectionItem, )))
    points = fields.ChoiceValueField(default_value='alpha', choices=('alpha', 'numbers', 'roman',))
    order = fields.ChoiceValueField(default_value='az', choices=('az', 'za'), blank=False)


SETS = {
    'all': (FreeformSection, ListSection, )
}
