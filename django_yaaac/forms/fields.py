from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.forms.models import ModelChoiceField
from django_yaaac.forms.widgets import AutocompleteWidget
from django import VERSION as DJ_VERSION


class AutocompleteModelChoiceField(ModelChoiceField):
    widget = AutocompleteWidget

    # TODO: passer admin_site en params.
    def __init__(self, site, queryset, empty_label="---------", cache_choices=False,
                 required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, *args, **kwargs):
        app_label = queryset.model._meta.app_label
        if DJ_VERSION < (1, 6):
            info = (app_label, queryset.model._meta.module_name)
        else:
            info = (app_label, queryset.model._meta.model_name)
        if True: # We want to use Admin changelist for FK lookup. TODO
            self.lookup_url = reverse_lazy('admin:%s_%s_changelist' % info,
                                           current_app=site.name)
        
        content_type_id = ContentType.objects.get_for_model(queryset.model).id
        self.search_url = reverse_lazy("yaaac:search",
                                       kwargs={"content_type_id": content_type_id})
        ModelChoiceField.__init__(self, queryset, empty_label, cache_choices,
                                  required, widget, label, initial, help_text,
                                  to_field_name, *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(AutocompleteModelChoiceField, self).widget_attrs(widget)
        attrs.update({
            'search_url': self.search_url,
            'lookup_url': self.lookup_url, 
        })
        return attrs
