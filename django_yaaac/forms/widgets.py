from builtins import str
import json

from django import VERSION as DJ_VERSION
from django import forms
from django.contrib.admin.templatetags.admin_static import static
if DJ_VERSION < (1, 10):
    from django.core.urlresolvers import reverse_lazy
else:
    from django.urls import reverse_lazy
from django.forms.utils import flatatt
from django.forms import Media
from django.utils.html import format_html
from django.utils.text import Truncator
from django_yaaac.utils import clean_fieldname_prefix


JS_COMPAT_FILE = "yaaac_compat.js"


class AutocompleteWidget(forms.HiddenInput):
    is_hidden = False

    @property
    def media(self):
        css = {
            'all': (
                'django_yaaac/css/autocomplete.css',
            )
        }
        js = (
            'django_yaaac/js/jquery.autocomplete.min.js',
            'django_yaaac/js/%s' % JS_COMPAT_FILE,
            'django_yaaac/js/yaaac_autocomplete.js',
        )
        base_media = super(AutocompleteWidget, self).media
        media = Media(js=[static(path) for path in js],
                      css=dict([
                          (key, [static(path) for path in paths])
                          for key, paths in css.items()
                      ]))
        return base_media + media

    def __init__(self, attrs=None):
        self.queryset_id = None
        self.site = None
        self.model = None
        self.opts = None
        self.limit_choices_to = None
        super(AutocompleteWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        info = (self.site.name, app_label, model_name)
        if self.queryset_id is not None:
            search_url = reverse_lazy("yaaac:search_with_queryset_id",
                                      kwargs={"app": app_label,
                                              "model": model_name,
                                              "queryset_id": self.queryset_id})
        else:
            search_url = reverse_lazy("yaaac:search",
                                      kwargs={"app": app_label,
                                              "model": model_name})

        # Cannot just do self.opts.pop("search_fields") because render() must be side-effect free.
        search_fields = self.opts.get("search_fields")
        search_opts = self.opts.copy()
        del search_opts["search_fields"]

        # https://code.djangoproject.com/ticket/24252#ticket
        lookup_url = reverse_lazy('%s:%s_%s_changelist' % info, current_app=self.site.name)
        params = self.url_parameters()
        url_params = '?' + '&'.join('%s=%s' % (k, v) for k, v in params.items())

        attrs.update({
            'class': 'yaaac_%s yaaac_pk vForeignKeyRawIdAdminField' % clean_fieldname_prefix(name),
            'search_url': u"{search_url}{url_params}&suggest_by={suggest_by}".format(search_url=str(search_url),
                                                                                     url_params=url_params,
                                                                                     suggest_by=self.opts["suggest_by"]),
            'search_opts': json.dumps(search_opts),
            'search_fields': ",".join(search_fields),
        })
        hidden_input = super(AutocompleteWidget, self).render(name, value, attrs)
        autocomp_input_attrs = {
            "type": "text",
            "class": "yaaac_search_input",
            "placeholder": "start typing to search",
            "style": value and "display:none" or ""
        }
        # flatatt in Django < 1.11 does not handle None values.
        if not value and "required" in attrs:
            autocomp_input_attrs["required"] = ""
        autocomp_input = format_html('<input{0} />', flatatt(autocomp_input_attrs))
        lookup_elem = ''
        if self.opts['allow_lookup'] is True:
            lookup_elem = format_html('<a {0}><img {1} /></a>',
                                      flatatt({"href": u"{lookup_url}{url_params}".format(lookup_url=lookup_url,
                                                                                          url_params=url_params),
                                               "id": "lookup_id_%s" % name,
                                               "class": "yaaac_lookup",
                                              "style": value and "display:none" or ""}),
                                      flatatt({"width": "16", "height": "16", "alt": "Lookup",
                                               "src": static('django_yaaac/img/selector-search.gif')}))

        return format_html(u'<span class="yaaac_container{}">{}{}{}{}</span>',
                           ' {}'.format(self.attrs['class']) if 'class' in self.attrs else '',
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
        params.update({TO_FIELD_VAR: "id"})  # Hardcoded here because we do not have 'rel' object.
        return params
