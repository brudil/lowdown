import uuid
from typing import Dict

from spectrum.fields import Field


class BaseMetaclass(type):

    @classmethod
    def _get_fields(cls, bases, attrs):
        pass

    def __new__(cls, name, bases, attrs):
        fields = {}  # type: Dict[str, Field]
        for field_name, field_value in attrs.items():
            if isinstance(field_value, Field):
                fields[field_name] = field_value

        for base in reversed(bases):
            if hasattr(base, '_fields'):
                fields = {**fields, **base._fields}

        attrs['_fields'] = fields

        for field_name, field in fields.items():
            attrs[field_name] = field.create_default_value()

        return super(BaseMetaclass, cls).__new__(cls, name, bases, attrs)


class BaseElement(object, metaclass=BaseMetaclass):

    def __init__(self, **kwargs):
        self._id = str(uuid.uuid4())

        for fieldName, field in self._fields.items():
            if fieldName in kwargs:
                setattr(self, fieldName, kwargs[fieldName])

    def serialize_field(self, field_name: str):
        return self._fields[field_name].to_json(getattr(self, field_name))

    def to_json(self) -> Dict:
        output = dict()
        for field_name, field in self._fields.items():
            output[field_name] = field.to_json(getattr(self, field_name))

        return output

    def get_elements(self) -> list:
        found = []
        for field_name, field in self._fields.items():
            field_value = getattr(self, field_name)
            if isinstance(field_value, BaseElement):
                found.append(field_value)
                found.extend(field_value.get_elements())
            else:
                if isinstance(field_value, list):
                    for stream_element in field_value:
                        if isinstance(stream_element, BaseElement):
                            found.append(stream_element)
                            found.extend(stream_element.get_elements())
        return found

    def parse(self, structure: Dict):
        if '_id' in structure:
            self._id = structure['_id']
        else:
            raise ValueError('no id in structure')
        for field_name, field in self._fields.items():
            # print(field_name, field, structure, structure[field_name])
            if field_name not in structure:
                raise KeyError('{} not in structure {}'.format(field_name, structure))

            setattr(self, field_name, field.parse(structure[field_name]))

    def is_valid(self) -> bool:
        for field_name, field in self._fields.items():
            if not field.is_valid(getattr(self, field_name)):
                return False

        return True

    def get_uuid(self):
        return self._id
