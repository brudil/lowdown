import hashlib
from django.contrib.auth.models import AbstractUser


class LowdownUser(AbstractUser):
    pass

    @property
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
