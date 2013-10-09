from django.contrib import admin
from django.contrib.admin.templatetags.admin_static import static
from test_app import models
from test_app.views import BandMemberForm, BandMemberLimitForm


class AutocompleteAdmin(admin.AdminSite):
    pass


class BandAdmin(admin.ModelAdmin):
    pass


class BandMemberAdmin(admin.ModelAdmin):
    form = BandMemberForm
    
    class Media:
        js = (static('js/jquery.min.js'), )


autocomplete_site = AutocompleteAdmin(name='autocomplete-admin')
autocomplete_site.register(models.MusicGenre)
autocomplete_site.register(models.Band, BandAdmin)
autocomplete_site.register(models.BandMember, BandMemberAdmin)


class LimitChoicesBandMemberAdmin(BandMemberAdmin):
    form = BandMemberLimitForm
    

limit_choices_site = AutocompleteAdmin(name='limit-choices-admin')
limit_choices_site.register(models.MusicGenre)
limit_choices_site.register(models.Band, BandAdmin)
limit_choices_site.register(models.BandMember, LimitChoicesBandMemberAdmin)
