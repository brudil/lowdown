from django.contrib import admin
from django.contrib.admin import register

from .models import Multimedia, MultimediaImage


@register(Multimedia)
class MultimediaModelAdmin(admin.ModelAdmin):
    pass


@register(MultimediaImage)
class MultimediaImageModelAdmin(admin.ModelAdmin):
    pass
