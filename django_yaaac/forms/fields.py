from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.forms.models import ModelChoiceField
from django_yaaac.forms.widgets import AutocompleteWidget
from django import VERSION as DJ_VERSION


class AutocompleteModelChoiceField(ModelChoiceField):
    widget = AutocompleteWidget

    def __init__(self, site, queryset, yaaac_opts, empty_label="---------",
                 cache_choices=False, required=True, widget=None, label=None,
                 initial=None, help_text='', to_field_name=None, *args, **kwargs):
        app_label = queryset.model._meta.app_label
        if DJ_VERSION < (1, 6):
            info = (site.name, app_label, queryset.model._meta.module_name)
        else:
            info = (site.name, app_label, queryset.model._meta.model_name)
        
        content_type_id = ContentType.objects.get_for_model(queryset.model).id
        self.search_url = reverse_lazy("yaaac:search",
                                       kwargs={"content_type_id": content_type_id})
        self.value_attr = yaaac_opts["value_attr"]
        ModelChoiceField.__init__(self, queryset, empty_label, cache_choices,
                                  required, widget, label, initial, help_text,
                                  to_field_name, *args, **kwargs)
        self.widget.model = queryset.model
        # This use the admin changelist for related lookup in a popup.
        # If you want to provide your own mechanism, you can use a site object
        # that can provide a 'name' attribute and a view called by the following reverse.
        self.widget.lookup_url = reverse_lazy('%s:%s_%s_changelist' % info,
                                               current_app=site.name)

    def widget_attrs(self, widget):
        attrs = super(AutocompleteModelChoiceField, self).widget_attrs(widget)
        attrs.update({
            'search_url': self.search_url,
            'value_attr': self.value_attr, 
            'class': 'yaaac_pk vForeignKeyRawIdAdminField',
        })
        return attrs
