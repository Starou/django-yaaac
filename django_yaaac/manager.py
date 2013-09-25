from django.contrib.contenttypes.models import ContentType
from django_yaaac.shortcuts import json_response


class AutocompleteManager(object):
    def __init__(self, name="yaaac", app_name="yaaac"):
        self.name = name
        self.app_name = app_name

    def get_urls(self):
        from django.conf.urls import patterns, url
        urlpatterns = patterns('',
            url(r'^(?P<content_type_id>\d+)/search/$', self.search, name='search'),
        )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    def search(self, request, content_type_id):
        klass = ContentType.objects.get_for_id(id=content_type_id).model_class()

        query = request.GET.get('query')
        result = klass.objects.filter(name__istartswith=query).values_list('id', 'name') or [('', '')]
        data, suggestions = zip(*result)
        return json_response({'query': request.GET.get('query'),
                              'suggestions': suggestions,
                              'data': data})


autocomplete = AutocompleteManager()
