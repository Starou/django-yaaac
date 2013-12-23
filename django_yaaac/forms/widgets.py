import json
from django import VERSION as DJ_VERSION
from django import forms
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse_lazy
if DJ_VERSION < (1, 7):
    from django.forms.util import flatatt
else:
    from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.text import Truncator
from django_yaaac.utils import clean_fieldname_prefix



JS_COMPAT_FILE = "yaaac_compat.js"
if DJ_VERSION < (1, 6):
    JS_COMPAT_FILE = "yaaac_compat_legacy.js"


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
            static('django_yaaac/js/%s' % JS_COMPAT_FILE),
            static('django_yaaac/js/yaaac_autocomplete.js'),
        )

    def __init__(self, site, model, limit_choices_to=None, opts=None, attrs=None):
        self.site = site
        self.model = model
        self.opts = {
            "min_chars": 1,
            "max_height": 300,
            "width": 300,
            "suggest_by": "__unicode__",
        }
        # opts should not by None.
        self.opts.update(opts)

        self.limit_choices_to = limit_choices_to or {}
        super(AutocompleteWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        app_label = self.model._meta.app_label
        if DJ_VERSION < (1, 6):
            model_name = self.model._meta.module_name
        else:
            model_name = self.model._meta.model_name
        info = (self.site.name, app_label, model_name)
        search_url = reverse_lazy("yaaac:search", kwargs={"app": app_label, "model": model_name})
        
        # Cannot just do self.opts.pop("search_fields") because render() must be side-effect free.
        search_fields = self.opts.get("search_fields")
        search_opts = self.opts.copy()
        del search_opts["search_fields"]

        lookup_url = reverse_lazy('%s:%s_%s_changelist' % info, current_app=self.site.name)
        params = self.url_parameters()
        url_params = '?' + '&'.join('%s=%s' % (k, v) for k, v in params.items())

        attrs.update({
            'class': 'yaaac_%s yaaac_pk vForeignKeyRawIdAdminField' % clean_fieldname_prefix(name),
            'search_url': "%s%s&suggest_by=%s" % (search_url, url_params, self.opts["suggest_by"]),
            'search_opts': json.dumps(search_opts),
            'search_fields': ",".join(search_fields), 
        })
        hidden_input = super(AutocompleteWidget, self).render(name, value, attrs)
        autocomp_input = format_html('<input{0} />',
                                     flatatt({"type": "text",
                                              "class": "yaaac_search_input",
                                              "placeholder": "start typing to search",
                                              "style": value and "display:none" or ""}))
        lookup_elem = format_html('<a {0}><img {1} /></a>',
                                  flatatt({"href": "%s%s" % (lookup_url, url_params),
                                           "id": "lookup_id_%s" % name,
                                           "class": "yaaac_lookup",
                                          "style": value and "display:none" or ""}),
                                  flatatt({"width": "16", "height": "16", "alt": "Lookup",
                                           "src": static('django_yaaac/img/selector-search.gif')}))
        
        return format_html(u'<span class="yaaac_container">{0}{1}{2}{3}</span>',
                           hidden_input, autocomp_input, lookup_elem, self.value_elem(value))

    def value_elem(self, value):
        style = 'display:none'
        label = hasattr(self.model, "get_absolute_url") and format_html('<a></a>') or ''
        clear_elem = format_html('<span class="yaaac_clear_value">x</span>')
        if value:
            obj = self.model._default_manager.get(pk=value)
            label = Truncator(obj).words(14, truncate=" ...")
            style = ''
            try:
                url = obj.get_absolute_url()
            except AttributeError:
                pass
            else:
                label = format_html(u'<a{0}>{1}</a>', flatatt({"href": url}), label)
        label_elem = format_html(u'<span{0}>{1}</span>', flatatt({"class": "yaaac_value"}), label)
        return format_html(u'<span{0}>{1}{2}</span>',
                           flatatt({"class": "yaaac_value_container", "style": style}),
                           label_elem, clear_elem)

    def base_url_parameters(self):
        from django.contrib.admin.widgets import url_params_from_lookup_dict
        return url_params_from_lookup_dict(self.limit_choices_to)

    def url_parameters(self):
        from django.contrib.admin.views.main import TO_FIELD_VAR
        params = self.base_url_parameters()
        params.update({TO_FIELD_VAR: "id"}) # Hardcoded here because we do not have 'rel' object.
        return params
