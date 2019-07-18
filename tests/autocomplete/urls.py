from __future__ import absolute_import
from django_yaaac.manager import autocomplete
from django.conf.urls import url
from django.contrib import admin

from autocomplete import views

urlpatterns = [
    url('^admin/', admin.site.urls),
    url(r'^yaaac/', autocomplete.urls),
    url(r'^band-member-form/$', views.band_member_form),
    url(r'^band-member-form/(?P<member_id>\d+)/$', views.band_member_form),
    url(r'^band-member-form/limit-choices/$', views.band_member_limit_form),
    url(r'^band-member-form/limit-choices/(?P<member_id>\d+)/$', views.band_member_limit_form),
    url(r'^band-member-form/extra-css/$', views.band_member_extra_css),
    url(r'^band-member-form/no-lookup/$', views.band_member_no_lookup),
]
