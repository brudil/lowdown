from django.db import models
from lowdown.core.verticals.fields import VerticalField


class Author(models.Model):
    class Meta:
        db_table = 'author'

    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField(null=False)
    vertical = VerticalField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
