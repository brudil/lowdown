from django.db import models

from lowdown.core.users.models import LowdownUser


class ReleaseNote(models.Model):
    user = models.ForeignKey(LowdownUser)
    version_number = models.CharField(max_length=32)
    body = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
