from spectrum import fields
from spectrum import subtypes
from spectrum.base import BaseElement


class SpectrumDocument(BaseElement):
    class Meta:
        pass

    version = 1
    type = 'spectrum'

    content = fields.ElementField(limit_to=subtypes.SETS['all'])

    def to_json(self):
        if not self.is_valid():
            raise ValueError('Can not serialize invalid state')

        return {
            'version': self.version,
            'content': self.serialize_field('content'),
            '_id': self._id
        }

    @classmethod
    def from_json(cls, structure):
        document = SpectrumDocument()
        document.parse(structure)
        return document
