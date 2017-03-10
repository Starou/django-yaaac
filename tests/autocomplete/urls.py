from django_yaaac.manager import autocomplete
from django.conf.urls import patterns, include, url

from my_admin import limit_choices_site, autocomplete_site

urlpatterns = patterns('',
    (r'^limit-choices-admin/', include(limit_choices_site.urls)),
    (r'^admin/', include(autocomplete_site.urls)),
    url(r'^yaaac/', include(autocomplete.urls)),
    url(r'^band-member-form/$', "autocomplete.views.band_member_form"),
    url(r'^band-member-form/(?P<member_id>\d+)/$', "autocomplete.views.band_member_form"),
    url(r'^band-member-form/limit-choices/$', "autocomplete.views.band_member_limit_form"),
    url(r'^band-member-form/limit-choices/(?P<member_id>\d+)/$', "autocomplete.views.band_member_limit_form"),
)
