from typing import Iterable, Tuple, Optional, Any, Dict
import abc


class Field(object):

    @abc.abstractmethod
    def to_json(self, value) -> Dict:
        return

    @abc.abstractmethod
    def create_default_value(self) -> Any:
        return

    @abc.abstractmethod
    def is_valid(self, value) -> bool:
        return True

    def parse(self, structure):
        pass


class ElementField(Field):
    type = 'field'

    def __init__(self, limit_to: Iterable, default_element=None, blank=False):
        self.limit_to = limit_to
        self.default_element = default_element
        self.blank = blank

    def to_json(self, value):
        if value is None:
            return None

        return {
            '_name': value.Meta.name,
            '_id': value.get_uuid(),
            **value.to_json()
        }

    def create_default_value(self):
        if self.default_element is None:
            return None

        return self.default_element()

    def is_valid(self, value):
        return True

    def parse(self, structure):
        if structure is None:
            if self.blank is True:
                return None
            else:
                raise ValueError('Structure is illegally none')

        name = structure['_name']
        element = None
        for elementOption in self.limit_to:
            if elementOption.Meta.name == name:
                element = elementOption
                break

        if element is None:
            raise ValueError(name, self)

        element = element()
        element.parse(structure)

        return element


class FieldStreamField(Field):
    type = 'stream'

    def __init__(self, item_field):
        self.item_field = item_field

    def create_default_value(self):
        return []

    def to_json(self, value: Iterable) -> Iterable[dict]:
        return [self.item_field.to_json(value_item) for value_item in value]

    def is_valid(self, value):
        for value_item in value:
            if not self.item_field.is_valid(value_item):
                return False

        return True

    def parse(self, structure):
        return [self.item_field.parse(item) for item in structure]


class ValueField(Field):
    def to_json(self, value):
        return value

    def parse(self, structure):
        return structure


class IntegerValueField(ValueField):
    def create_default_value(self) -> Any:
        return None

    def is_valid(self, value) -> bool:
        return isinstance(value, int)


class StringValueField(ValueField):
    def create_default_value(self) -> Any:
        return None

    def is_valid(self, value) -> bool:
        return isinstance(value, str)


class ChoiceValueField(ValueField):

    def __init__(self, default_value: Any=None, choices: Optional[Tuple[Any, ...]]=None, blank: bool=False):
        super().__init__()
        self.default_value = default_value
        self.choices = choices
        self.blank = blank

    def create_default_value(self) -> Any:
        if self.default_value:
            return self.default_value

        return None

    def is_valid(self, value):
        if self.blank is True and value is None:
            return False

        if value not in self.choices:
            return False

        return True


class URLValueField(ValueField):
    def __init__(self, blank=False):
        self.blank = blank

    def create_default_value(self) -> Any:
        return None

    def is_valid(self, value):
        if not self.blank and value is None:
            return False
        return True


class TransformerInterface(object):
    def __init__(self, transformer, text=''):
        self.transformer = transformer
        self.text = text

    def get_transformer_name(self):
        print('transformer', self)
        return self.transformer.Meta.name

    def get_text(self):
        return self.text


class TextualContentField(Field):
    def __init__(self, default_transformer, limit_to=None):
        if default_transformer is None:
            raise ValueError('default transformer needed')
        self.default_transformer = default_transformer
        if limit_to is None:
            limit_to = (default_transformer, )
        self.limit_to = limit_to

    def to_json(self, value):
        return {
            '_name': 'text',
            'transformer': value.get_transformer_name(),
            'text': value.get_text()
        }

    def create_default_value(self):
        return TransformerInterface(self.default_transformer)

    def map_transformer_to_name(self, name):
        default_transformer_name = self.default_transformer.Meta.name;
        if name == default_transformer_name:
            return self.default_transformer

        raise ValueError('"{}" is not default transformer ({})'.format(name, default_transformer_name))

    def parse(self, structure):
        return TransformerInterface(self.map_transformer_to_name(structure['transformer']), structure['text'])

    def is_valid(self, value):
        return True
