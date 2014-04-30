from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_yaaac.forms.fields import AutocompleteModelChoiceField
from test_app import models


## Forms ##

class BandMemberForm(forms.ModelForm):
    band = AutocompleteModelChoiceField(site=admin.site, queryset=models.Band.objects.all(),
                                        yaaac_opts={
                                            "search_fields": ["^name"],
                                            "min_chars": 3,
                                            "suggest_by": "get_full_info",
                                        }, required=True)

    class Meta:
        model = models.BandMember
        exclude = ()


class BandMemberLimitForm(forms.ModelForm):
    band = AutocompleteModelChoiceField(site=admin.site, queryset=models.Band.objects.all(),
                                        limit_choices_to={"genre__name__in": ["Rock", "Blues/Rock"]},
                                        yaaac_opts={
                                            "search_fields": ["^name"],
                                            "suggest_by": "name",
                                        }, required=True)

    class Meta:
        model = models.BandMember
        exclude = ()


class BandMemberInlineForm(forms.ModelForm):
    favorite_instrument = AutocompleteModelChoiceField(label="Favorite instrument", site=admin.site,
                                                       queryset=models.Instrument.objects.all(),
                                                       yaaac_opts={
                                                           "search_fields": ["^name"],
                                                           "min_chars": 3,
                                                           "max_height": 200,
                                                           "width": 150,
                                                       }, required=False)

    class Meta:
        model = models.BandMember
        exclude = ()


## Views ##

def band_member_form(request, member_id=None):
    band_member = None
    if member_id:
        band_member = models.BandMember.objects.get(pk=member_id)
    form = BandMemberForm(request.POST or None, instance=band_member)
    if request.method == 'POST':
        band_member = form.save()
        return HttpResponseRedirect("/band-member-form/%s/" % band_member.pk)
    return render_to_response('base_form.html', {
        'form': form,
        'title': "Add a band member"
    }, context_instance=RequestContext(request))


def band_member_limit_form(request, member_id=None):
    band_member = None
    if member_id:
        band_member = models.BandMember.objects.get(pk=member_id)
    form = BandMemberLimitForm(request.POST or None, instance=band_member)
    if request.method == 'POST':
        band_member = form.save()
        return HttpResponseRedirect("/band-member-form/limit-choices/%s/" % band_member.pk)
    return render_to_response('base_form.html', {
        'form': form,
        'title': "Add a band member"
    }, context_instance=RequestContext(request))
