from django.contrib import admin
from . import models

admin.site.register(models.Instrument)
admin.site.register(models.MusicGenre)
admin.site.register(models.Band)
admin.site.register(models.BandMember)
