from django.db import models
from lowdown.core.verticals.fields import VerticalField


class Section(models.Model):
    class Meta:
        db_table = 'section'

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    vertical = VerticalField()

    parent = models.ForeignKey('self', null=True, blank=True, default=None)

    title = models.TextField(null=False)
    slug = models.SlugField(unique=False, null=False, blank=False)

    deleted = models.BooleanField(default=False)


    class Meta:
        unique_together = ('vertical', 'slug',)

    def __str__(self):
        return self.title
