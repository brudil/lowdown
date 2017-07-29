from django.db import models


class Interactive(models.Model):
    revision_count = models.PositiveIntegerField(default=0, null=False)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.slug

    def get_latest_public_release(self):
        return self.releases.filter(public=True).latest('created')

class InteractiveRelease(models.Model):
    interactive = models.ForeignKey(Interactive, null=False, related_name='releases')
    created = models.DateTimeField(auto_now_add=True)
    revision_number = models.PositiveIntegerField(null=False, default=0)

    public = models.BooleanField(default=False)

    def __str__(self):
        return '{}, v{} - {}'.format(self.interactive, self.revision_number, 'PUBLIC' if self.public else 'INTERNAL')
