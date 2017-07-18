from django.db import models


class Topic(models.Model):
    class Meta:
        db_table = 'topic'

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    section = models.ForeignKey('sections.Section', null=False)

    title = models.TextField(null=False)
    slug = models.SlugField(unique=True, null=False, blank=False)

    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
