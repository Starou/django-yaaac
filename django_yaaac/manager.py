from builtins import str
from builtins import object
import operator
from django.contrib.admin.views.main import TO_FIELD_VAR
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django_yaaac.shortcuts import json_response
from django_yaaac.utils import lookup_dict_from_url_params
from functools import reduce


def cache_model(f):
    def wrapper(manager, request, *args, **kwargs):
        app = kwargs["app"]
        model = kwargs["model"]
        kwargs["model"] = ContentType.objects.get(app_label=app,
                                                  model=model).model_class()
        return f(manager, request, *args, **kwargs)
    return wrapper


def check_permissions(f):
    def wrapper(manager, request, *args, **kwargs):
        model = kwargs["model"]
        suggest_by = request.GET.get('suggest_by')
        try:
            options = model.Yaaac()
            options.user_passes_test
            options.allows_suggest_by
        except AttributeError:
            return HttpResponseNotFound()
        if not options.user_passes_test(request.user):
            return HttpResponseForbidden()
        if not suggest_by and not request.GET.get("pk"):
            return HttpResponseNotFound()
        if suggest_by and suggest_by not in options.allows_suggest_by:
            return HttpResponseForbidden()

        return f(manager, request, *args, **kwargs)
    return wrapper


class AutocompleteManager(object):
    def __init__(self, name="yaaac", app_label="yaaac"):
        self.name = name
        self.app_label = app_label
        self.registered_querysets = {}

    def get_urls(self):
        from django.conf.urls import url
        return [
            url(r'^(?P<app>\w+)/(?P<model>\w+)/(?P<queryset_id>\d+)/search/$',
                self.search, name='search_with_queryset_id'),
            url(r'^(?P<app>\w+)/(?P<model>\w+)/search/$', self.search, name='search'),
        ]

    @property
    def urls(self):
        return self.get_urls(), self.app_label, self.name

    @cache_model
    @check_permissions
    def search(self, request, app, model, queryset_id=None):
        query = request.GET.get('query')
        pk = request.GET.get('pk')
        if pk:
            obj = model.objects.get(pk=pk)
            try:
                url = obj.get_absolute_url()
            except AttributeError:
                url = None
            return json_response({
                "value": str(obj),
                "url": url,
            })
        search_fields = request.GET.get('search_fields').split(",")
        suggest_by = request.GET.get('suggest_by')

        filter_params = request.GET.copy()
        del filter_params[TO_FIELD_VAR]
        del filter_params["query"]
        del filter_params["search_fields"]
        if "suggest_by" in filter_params:
            del filter_params["suggest_by"]
        kwargs = lookup_dict_from_url_params(filter_params)
        if queryset_id is not None:
            model_name = model._meta.model_name
            uuid = '%s-%s-%s' % (app, model_name, queryset_id)
            result = self.registered_querysets[uuid].filter(**kwargs)
        else:
            result = model.objects.filter(**kwargs)
        result = self.get_search_results(result, search_fields, query)

        if suggest_by in [f.name for f in model._meta.get_fields()]:
            result = result.values_list('id', suggest_by)
        else:
            result = [(o.pk, getattr(o, suggest_by)()) for o in result]
        result = result or [('', '')]
        suggestions = [{"value": r[1], "data": r[0]} for r in result]
        return json_response({'query': request.GET.get('query'),
                              'suggestions': suggestions})

    # From https://github.com/django/django/blob/master/django/contrib/admin/options.py
    # without the use_distinct calculation.
    def get_search_results(self, queryset, search_fields, search_term):
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        orm_lookups = [construct_search(str(search_field))
                       for search_field in search_fields]
        for bit in search_term.split():
            or_queries = [models.Q(**{orm_lookup: bit})
                          for orm_lookup in orm_lookups]
            queryset = queryset.filter(reduce(operator.or_, or_queries))
        return queryset

    def register_queryset(self, app_label, model_name, queryset):
        queryset_id = 0
        while True:
            uuid = '%s-%s-%s' % (app_label, model_name, queryset_id)
            if not uuid in self.registered_querysets:
                self.registered_querysets[uuid] = queryset
                break
            else:
                queryset_id += 1
        return queryset_id

autocomplete = AutocompleteManager()
