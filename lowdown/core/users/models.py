import hashlib
from django.contrib.auth.models import AbstractUser, Permission


class LowdownUser(AbstractUser):
    pass

    @property
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    @property
    def permissions(self):
        if self.is_superuser:
            return Permission.objects.all()
        return self.user_permissions.all() | Permission.objects.filter(group__user=user)
