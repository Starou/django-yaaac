from django.contrib import admin
from test_app import models


class BandAdmin(admin.ModelAdmin):
    pass


class BandMemberAdmin(admin.ModelAdmin):
    raw_id_fields = ("band",)


admin.site.register(models.MusicGenre)
admin.site.register(models.Band, BandAdmin)
admin.site.register(models.BandMember, BandMemberAdmin)
