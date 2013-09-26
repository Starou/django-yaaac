import django_yaaac as yaaac
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^yaaac/', include(yaaac.autocomplete.urls)),
    url(r'^$', "test_app.views.band_member_form"),
)
