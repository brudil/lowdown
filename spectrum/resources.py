from spectrum.base import BaseElement
from spectrum import fields


class Resource(BaseElement):
    class Meta:
        type = 'resource'

    id = fields.IntegerValueField()


class LowdownImageResource(Resource):
    class Meta:
        name = 'lowdownimage'


class OEmbedResource(Resource):
    class Meta:
        name = 'oembed'
