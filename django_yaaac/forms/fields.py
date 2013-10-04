from django.forms.models import ModelChoiceField
from django_yaaac.forms.widgets import AutocompleteWidget


class AutocompleteModelChoiceField(ModelChoiceField):
    widget = AutocompleteWidget

    def __init__(self, site, queryset, yaaac_opts, empty_label="---------",
                 cache_choices=False, required=True, widget=None, label=None,
                 initial=None, help_text='', to_field_name=None, *args, **kwargs):
        model = queryset.model
        widget = AutocompleteWidget(site, model, opts=yaaac_opts)
        ModelChoiceField.__init__(self, queryset, empty_label, cache_choices,
                                  required, widget, label, initial, help_text,
                                  to_field_name, *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(AutocompleteModelChoiceField, self).widget_attrs(widget)
        attrs.update({
            'class': 'yaaac_pk vForeignKeyRawIdAdminField',
        })
        return attrs
