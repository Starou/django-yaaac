from django.contrib import admin
from django.contrib.admin.templatetags.admin_static import static
from test_app import models
from test_app.views import BandMemberForm


class BandAdmin(admin.ModelAdmin):
    pass


class BandMemberAdmin(admin.ModelAdmin):
    form = BandMemberForm
    
    class Media:
        js = (static('js/jquery.min.js'), )


admin.site.register(models.MusicGenre)
admin.site.register(models.Band, BandAdmin)
admin.site.register(models.BandMember, BandMemberAdmin)
