from django.forms.models import ModelChoiceField
from django_yaaac.forms.widgets import AutocompleteWidget


class AutocompleteModelChoiceField(ModelChoiceField):
    widget = AutocompleteWidget

    def __init__(self, site, queryset, yaaac_opts, limit_choices_to=None,
                 empty_label="---------", cache_choices=False, required=True,
                 widget=None, label=None, initial=None, help_text='',
                 to_field_name=None, *args, **kwargs):
        # the `limit_choices_to' parameter allows us to enable the filtering in
        # the ajax autocomplete and the related lookup.
        # It may seems redundant with `ForeignKey.limit_choices_to' but we don't 
        # have access to a `rel' object here.
        model = queryset.model
        widget = AutocompleteWidget(site, model, limit_choices_to, yaaac_opts)
        ModelChoiceField.__init__(self, queryset, empty_label, cache_choices,
                                  required, widget, label, initial, help_text,
                                  to_field_name, *args, **kwargs)
