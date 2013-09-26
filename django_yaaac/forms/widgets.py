from django import forms
from django.contrib.admin.templatetags.admin_static import static
from django import VERSION as DJ_VERSION
if DJ_VERSION < (1, 6):
    from django.forms.util import flatatt
else:
    from django.forms.utils import flatatt
from django.utils.html import format_html


class AutocompleteWidget(forms.HiddenInput):
    is_hidden = False

    class Media:
        css = {
            'all': (
                static('django_yaaac/css/autocomplete.css'),
            )
        }
        js = (
            static('django_yaaac/js/jquery.autocomplete.min.js'),
            static('django_yaaac/js/yaaac_autocomplete.js'),
        )

    def render(self, name, value, attrs=None):
        hidden_input = super(AutocompleteWidget, self).render(name, value, attrs)
        autocomp_input = format_html('<input{0} />',
                                     flatatt({"type": "text",
                                              "class": "yaaac_search_input" }))
        return format_html('<span class="yaaac_container">{0}{1}</span>',
                           hidden_input, autocomp_input)
