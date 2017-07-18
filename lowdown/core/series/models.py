from django.db import models


class Series(models.Model):
    class Meta:
        db_table = 'series'

    created = models.DateTimeField(auto_now_add=True)
    title = models.TextField(null=False)
    slug = models.SlugField()

    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
