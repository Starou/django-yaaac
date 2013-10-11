from django.contrib.contenttypes.models import ContentType
from django_yaaac.shortcuts import json_response
from django_yaaac.utils import lookup_dict_from_url_params


class AutocompleteManager(object):
    def __init__(self, name="yaaac", app_name="yaaac"):
        self.name = name
        self.app_name = app_name

    def get_urls(self):
        from django.conf.urls import patterns, url
        urlpatterns = patterns('',
            url(r'^(?P<app>\w+)/(?P<model>\w+)/search/$', self.search, name='search'),
        )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    def search(self, request, app, model):
        klass = ContentType.objects.get(app_label=app, model=model).model_class()

        query = request.GET.get('query')
        search_fields = request.GET.get('search_fields')
        suggest_by = request.GET.get('suggest_by') or search_fields
        pk = request.GET.get('pk')
        if pk:
            return json_response({
                "value": unicode(klass.objects.get(pk=pk))
            })

        filter_params = request.GET.copy()
        del filter_params["t"]
        del filter_params["query"]
        del filter_params["search_fields"]
        if "suggest_by" in filter_params:
            del filter_params["suggest_by"]
        kwargs = lookup_dict_from_url_params(filter_params)
        kwargs["%s__istartswith" % search_fields] = query

        result = klass.objects.filter(**kwargs)
        if suggest_by in klass._meta.get_all_field_names():
            result = result.values_list('id', search_fields)
        else:
            result = [(obj.pk, getattr(obj, suggest_by)()) for obj in result]
        result = result or [('', '')]
        suggestions = [{"value": r[1], "data": r[0]} for r in result]
        return json_response({'query': request.GET.get('query'),
                              'suggestions': suggestions})


autocomplete = AutocompleteManager()
