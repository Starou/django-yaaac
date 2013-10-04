import django_yaaac as yaaac
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^yaaac/', include(yaaac.autocomplete.urls)),
    url(r'^$', "test_app.views.band_member_form"),
    url(r'^(?P<member_id>\d+)/$', "test_app.views.band_member_form"),
    url(r'^band-member-form/limit-choices/$', "test_app.views.band_member_limit_form"),
    url(r'^band-member-form/limit-choices/(?P<member_id>\d+)/$', "test_app.views.band_member_limit_form"),
)
