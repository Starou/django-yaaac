from django_yaaac.manager import autocomplete
from django.urls import re_path
from django.contrib import admin

from autocomplete import views

urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path(r'^yaaac/', autocomplete.urls),
    re_path(r'^band-member-form/$', views.band_member_form),
    re_path(r'^band-member-form/(?P<member_id>\d+)/$', views.band_member_form),
    re_path(r'^band-member-form/limit-choices/$', views.band_member_limit_form),
    re_path(r'^band-member-form/limit-choices/(?P<member_id>\d+)/$', views.band_member_limit_form),
    re_path(r'^band-member-form/extra-css/$', views.band_member_extra_css),
    re_path(r'^band-member-form/no-lookup/$', views.band_member_no_lookup),
]
