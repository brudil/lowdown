from .models import Content, ContentRevision, ContentEditorialMetadata
from django.contrib import admin

admin.site.register(Content)
admin.site.register(ContentRevision)
admin.site.register(ContentEditorialMetadata)
