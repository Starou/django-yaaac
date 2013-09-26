from django import forms
from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_yaaac.forms.fields import AutocompleteModelChoiceField
from test_app import models

class BandMemberForm(forms.ModelForm):
    band = AutocompleteModelChoiceField(site=admin.site, 
                                        queryset=models.Band.objects.all(),
                                        yaaac_opts={
                                            "value_attr": "name"
                                        },
                                        required=True)
    class Meta:
        model = models.BandMember


def band_member_form(request):
    form = BandMemberForm
    return render_to_response('base_form.html', {
        'form': form,
        'title': "Form"
    }, context_instance=RequestContext(request))
