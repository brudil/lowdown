import hashlib
import uuid
from PIL import Image
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from taggit.managers import TaggableManager
import boto3
from lowdown.core.verticals.fields import VerticalField

SOURCE_METHOD_CHOICES = (
    ('UPLD', 'Upload'),
)


class MultimediaImage(models.Model):
    class Meta:
        db_table = 'multimedia_image'

    focus_point_x = models.FloatField(null=True, default=None)
    focus_point_y = models.FloatField(null=True, default=None)
    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)

    @classmethod
    def create_via_file(cls, file):
        instance = cls()

        im = Image.open(file)
        width, height = im.size

        instance.width = width
        instance.height = height

        instance.save()
        return instance


def hash_file_sha1(file_obj):
    sha1 = hashlib.sha1()
    while True:
        data = file_obj.read(8192)
        if not data:
            break
        sha1.update(data)
    file_obj.seek(0)
    return sha1.hexdigest()


def upload_file(file, resource_name):
    s3 = boto3.resource('s3')
    s3.Object('lowdown-media', resource_name).put(Body=file, ContentType=file.content_type, ACL='public-read')


def create_child_model(file):
    return MultimediaImage.create_via_file(file)


class Multimedia(models.Model):
    class Meta:
        db_table = 'multimedia'

    vertical = VerticalField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    hash = models.TextField(null=False, unique=True)
    resource_name = models.UUIDField()
    file_name = models.TextField(null=False)
    file_type = models.TextField(null=False)
    file_size = models.IntegerField(null=False)
    mime = models.TextField(null=False)
    credit_title = models.TextField(null=False, blank=True, default='')
    credit_url = models.URLField(null=False, blank=True, default='')
    source_method = models.CharField(max_length=4, choices=SOURCE_METHOD_CHOICES, default='UPLD')
    metadata = JSONField(default={}, blank=True)

    uploader = models.ForeignKey('users.LowdownUser', related_name='multimedia')
    tags = TaggableManager(blank=True)

    deleted = models.BooleanField(default=False)

    media_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    media_object = GenericForeignKey('media_type', 'object_id')

    @property
    def direct_url(self):
        return 'https://s3-eu-west-1.amazonaws.com/lowdown-media/{}'.format(self.resource_name)

    @classmethod
    def has_file_already(cls, file):
        file_hash = hash_file_sha1(file)

        existing = cls.objects.filter(hash=file_hash)
        if existing.count() > 0:
            return existing[0]

        return None


    @classmethod
    def create_and_upload(cls, file, user, vertical):
        child_model = create_child_model(file)

        file_hash = hash_file_sha1(file)

        resource_name = str(uuid.uuid4())
        upload_file(file, resource_name)

        media = Multimedia()
        media.resource_name = resource_name
        media.hash = file_hash
        media.vertical = vertical
        media.file_name = file.name
        media.file_size = file.size
        media.file_type = file.content_type.split('/')[0]
        media.mime = file.content_type
        media.uploader = user
        media.media_object = child_model
        media.save()

        return media
