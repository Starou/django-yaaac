from django.contrib import admin
from django.contrib.admin.templatetags.admin_static import static
from . import models
from .views import BandMemberForm, BandMemberInlineForm, BandMemberLimitForm


class AutocompleteAdmin(admin.AdminSite):
    pass


class BandMemberInline(admin.TabularInline):
    model = models.BandMember
    form = BandMemberInlineForm
    extra = 0

    class Media:
        js = (static('js/jquery.min.js'), )


class BandAdmin(admin.ModelAdmin):
    inlines = [BandMemberInline]


class BandMemberAdmin(admin.ModelAdmin):
    form = BandMemberForm

    class Media:
        js = (static('js/jquery.min.js'), )


autocomplete_site = AutocompleteAdmin(name='autocomplete-admin')
autocomplete_site.register(models.Instrument)
autocomplete_site.register(models.MusicGenre)
autocomplete_site.register(models.Band, BandAdmin)
autocomplete_site.register(models.BandMember, BandMemberAdmin)


## An Admin with 'limit_choices_to' set. ##


class LimitChoicesBandMemberAdmin(BandMemberAdmin):
    form = BandMemberLimitForm


limit_choices_site = AutocompleteAdmin(name='limit-choices-admin')
limit_choices_site.register(models.MusicGenre)
limit_choices_site.register(models.Band, BandAdmin)
limit_choices_site.register(models.BandMember, LimitChoicesBandMemberAdmin)
