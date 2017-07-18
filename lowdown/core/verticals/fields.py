from django.db import models
from lowdown.core.verticals.structure import MANAGER as VERTICAL_MANAGER


class VerticalField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(VerticalField, self).__init__(
            max_length=32,
            choices=VERTICAL_MANAGER.get_identifier_choices(),
            null=False,
            blank=False,
        )

    def deconstruct(self):
        name, path, args, kwargs = super(VerticalField, self).deconstruct()

        return name, path, args, kwargs
