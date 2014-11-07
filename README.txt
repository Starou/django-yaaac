===============================
Another Ajax Auto-Complete, Yet
===============================


.. image:: https://coveralls.io/repos/Starou/django-yaaac/badge.png
  :target: https://coveralls.io/r/Starou/django-yaaac

.. image:: https://pypip.in/v/django-yaaac/badge.png
  :target: https://pypi.python.org/pypi/django-yaaac

.. image:: https://pypip.in/py_versions/django-yaaac/badge.svg
    :target: https://pypi.python.org/pypi/django-yaaac/
    :alt: Supported Python versions

.. image:: https://pypip.in/license/django-yaaac/badge.svg
    :target: https://pypi.python.org/pypi/django-yaaac/
    :alt: License



*Yaaac* is lightweight Django application providing Ajax search to admin foreign-key form fields in addition 
to the *raw_id_fields* related lookup and - *cerise sur le gateau* - it is usable outside the admin.


Examples
========

In the admin
------------

Configure the admin form to enable Ajax search where you usually use *raw_id_fields*.

.. image:: examples/screenshot-admin-1.png
    :alt: Ajax search field 

Start typing to select a value from the suggestion.

.. image:: examples/screenshot-admin-2.png
    :alt: Ajax search in progress

The selected object is displayed using the unicode value. You can reset the field to choose another one.

.. image:: examples/screenshot-admin-3.png
    :alt: Ajax search completed

In inlines as well.

.. image:: examples/screenshot-admin-inline.png
    :alt: Ajax search in inlines


Installation
============

Install the app from the source::

    python setup.py build && (sudo) python setup.py install

Or with *pip*::

    pip install django-yaaac

Add the app in your settings.INSTALLED_APPS::

    INSTALLED_APPS = [
        ...,
        "django_yaaac",
        ...,
    ]

In the *urls.py* module of your project, define the url pattern for ajax calls::

    import django_yaaac as yaaac
    from django.conf.urls import patterns, include, url

    urlpatterns = patterns('',
        url(r'^yaaac/', include(yaaac.autocomplete.urls)),
        ...
    )


Usage
=====

Forms
-----

What you need to do is to declare a custom *ModelForm* and use it in your *ModelAdmin*::


    from django import forms
    from django.contrib import admin
    from django.contrib.admin.templatetags.admin_static import static
    from django.template import RequestContext
    from django_yaaac.forms.fields import AutocompleteModelChoiceField
    from test_app import models
    

    class BandMemberForm(forms.ModelForm):
        band = AutocompleteModelChoiceField(site=admin.site, 
                                            queryset=models.Band.objects.all(),
                                            yaaac_opts={
                                                "search_fields": ["^name"],
                                                "suggest_by": "get_full_name",
                                                "min_chars": 3,    # Fire search when 3 chars are sent (1 by default.)
                                                "max_height": 400, # 300px by default.
                                                "width": 250,      # 300px by default.
                                            },
                                            required=True)
        class Meta:
            model = models.BandMember


    class BandMemberAdmin(admin.ModelAdmin):
        form = BandMemberForm
        
        class Media:
            # You need jQuery.
            js = (static('js/jquery.min.js'), )


    admin.site.register(models.BandMember, BandMemberAdmin)


The *site* parameter of *AutocompleteModelChoiceField* is required for related lookup (the
magnifier glass). The *search_fields* is a list of fields to search against using the same syntax
as in Django Admin (^, $ etc).
Extra options *min_chars*, *max_height* and *width* are the counter-part of *minChars*, *maxHeight* and *width*
in `Autocomplete options <https://github.com/devbridge/jQuery-Autocomplete#api>`_.


Do not forget to add *jQuery* in your template (using *ModelAdmin.Media.js* in the example above).
Outside the admin, you have to explicitly call the yaaac static files like that::
    
    <head>
      {{ form.media }}
    </head>


*suggest_by* is optional. It can be a field or a method of the model.
By default, suggestions are shown using *__unicode__* method.

If your model define a ``get_absolute_url()`` method, the label is a link to that resource.


Models
------

For security reasons you must open the search view on the models like this::

    class BandMember(models.Model):
        plain_stupid_password = models.CharField(max_length=4)
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        band = models.ForeignKey("Band", null=True, blank=True)
        favorite_instrument = models.ForeignKey("Instrument", null=True, blank=True)

        class Meta:
            unique_together = (('first_name', 'last_name'),)

        class Yaaac:
            user_passes_test = lambda instance, user: user and user.is_authenticated() or False 
            allows_suggest_by = ['get_full_name']

        def __unicode__(self):
            return u"%s %s" % (self.first_name, self.last_name)

        def get_full_name(self):
            return u"%s %s" % (self.first_name, self.last_name)


The `Yaaac` class must defines the following:


- ``user_passes_test`` is a class method that takes a user and return True or False.
- ``allows_suggest_by`` is a list of model fields or methods that can used as return value by the search view.


Tuning
======


To ease the DOM manipulation, HTML classes are added to the elements. The most interesting being ``yaaac_<fieldname>``
to the hidden input storing the foreign key value. This is very convenient when you need to add behavior to a whole
set of fields - also those that don't exist when the page is created - sharing the same name. 

Use jQuery delegation (i.e. ``$(".foo").on("change", ".yaaac_first_name")``) to place an event on one field for all 
the inline forms present in the page or to come (i.e. Click on "Add a new Band Member".)
