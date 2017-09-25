from django.contrib import admin

from .models import ReleaseNote


class ReleaseNoteAdmin(admin.ModelAdmin):
    pass

admin.site.register(ReleaseNote, ReleaseNoteAdmin)
