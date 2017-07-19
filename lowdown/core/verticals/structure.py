from lowdown.core.content import constants

class Vertical:
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier


class VerticalManager:
    def __init__(self, verticals):
        self.verticals = verticals

    def verticals_by_key(self):
        d = dict()
        for vertical in self.verticals:
            d[vertical.identifier] = vertical

        return d

    def get_by_identifier(self, identifier):
        try:
            return self.verticals_by_key()[identifier]
        except KeyError:
            return None

    def get_identifier_choices(self):
        l = [(v.identifier, v.name) for v in self.verticals]

        return tuple(l)


class ThePrate(Vertical):
    name = 'The Prate'
    identifier = 'theprate'

    content_forms = [
        constants.FORM_ARTICLE,
        constants.FORM_GALLERY,
    ]

    content_tones = [
        constants.TONE_CONTENT,
        constants.TONE_REVIEW,
        constants.TONE_INTERACTIVE,
        constants.TONE_GUIDE,
    ]


class TheDrab(Vertical):
    name = 'The Drab'
    identifier = 'thedrab'

    content_forms = [
        constants.FORM_ARTICLE,
    ]

    content_tones = [
        constants.TONE_CONTENT,
    ]


MANAGER = VerticalManager((
    ThePrate,
    TheDrab,
))
