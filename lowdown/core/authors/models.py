from django.db import models
from lowdown.core.verticals.fields import VerticalField


class Author(models.Model):
    class Meta:
        db_table = 'author'

    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField(null=False)
    slug = models.SlugField(null=True, unique=False)
    bio = models.TextField(default='')
    vertical = VerticalField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
