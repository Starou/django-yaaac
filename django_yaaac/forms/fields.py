from django.forms.models import ModelChoiceField
from django_yaaac.forms.widgets import AutocompleteWidget
from django_yaaac.manager import autocomplete


class AutocompleteModelChoiceField(ModelChoiceField):
    widget = AutocompleteWidget

    def __init__(self, site, queryset, yaaac_opts, limit_choices_to=None,
                 empty_label="---------", cache_choices=None, required=True,
                 widget=None, label=None, initial=None, help_text='',
                 to_field_name=None, *args, **kwargs):
        # the `limit_choices_to' parameter allows us to enable the filtering in
        # the ajax autocomplete and the related lookup.
        # It may seems redundant with `ForeignKey.limit_choices_to' but we don't
        # have access to a `rel' object here.

        model = queryset.model

        app_label = model._meta.app_label
        model_name = model._meta.model_name
        queryset_id = autocomplete.register_queryset(app_label=app_label, model_name=model_name, queryset=queryset)

        widget = AutocompleteWidget(site, model, limit_choices_to, yaaac_opts, queryset_id=queryset_id)
        ModelChoiceField.__init__(self, queryset, empty_label,
                                  required, widget, label, initial, help_text,
                                  to_field_name, *args, **kwargs)
