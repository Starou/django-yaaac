from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from test_app import models

class BandMemberForm(forms.ModelForm):
    band = forms.ModelChoiceField(queryset=models.Band.objects.all(), required=True)
    class Meta:
        model = models.BandMember


def band_member_form(request):
    form = BandMemberForm()
    return render_to_response('base_form.html', {
        'form': form,
        'title': "Form"
    }, context_instance=RequestContext(request))
