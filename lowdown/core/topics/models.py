from django.db import models


class Topic(models.Model):
    class Meta:
        db_table = 'topic'

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    section = models.ForeignKey('sections.Section', null=False, related_name='topics', on_delete=models.CASCADE)

    title = models.TextField(null=False)
    slug = models.SlugField(null=False, blank=False)

    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('section', 'slug',)

    def __str__(self):
        return self.title
