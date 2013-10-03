from django import forms
from django.contrib.admin.templatetags.admin_static import static
from django import VERSION as DJ_VERSION
if DJ_VERSION < (1, 6):
    from django.forms.util import flatatt
else:
    from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.text import Truncator


class AutocompleteWidget(forms.HiddenInput):
    is_hidden = False
    model = None
    lookup_url = ""

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
                                              "class": "yaaac_search_input",
                                              "placeholder": "start typing to search",
                                              "style": value and "display:none" or ""}))
        lookup_elem = format_html('<a {0}><img {1}></img></a>',
                                  # FIXME: t=id is hardcoded and that's bad.
                                  # Should do something like in ForeignKeyRawIdWidget.url_parameters()
                                  # to filter on rel.limit_choices_to and self.limit_choices_to.
                                  flatatt({"href": "%s?t=id" % self.lookup_url,
                                           "id": "lookup_id_%s" % name,
                                           "class": "yaaac_lookup",
                                          "style": value and "display:none" or ""}),
                                  flatatt({"width": "16", "height": "16", "alt": "Lookup",
                                           "src": static('django_yaaac/img/selector-search.gif')}))
        
        return format_html('<span class="yaaac_container">{0}{1}{2}{3}</span>',
                           hidden_input, autocomp_input, lookup_elem, self.value_elem(value))

    def value_elem(self, value):
        style = 'display:none'
        label = ''
        clear_elem = format_html('<span class="yaaac_clear_value">x</span>')
        if value:
            obj = self.model._default_manager.get(pk=value)
            label = Truncator(obj).words(14, truncate=" ...")
            style = ''
        label_elem = format_html('<span{0}>{1}</span>', flatatt({"class": "yaaac_value"}), label)
        return format_html('<span{0}>{1}{2}</span>',
                           flatatt({"class": "yaaac_value_container", "style": style}),
                           label_elem, clear_elem)
