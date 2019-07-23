===============================
Another Ajax Auto-Complete, Yet
===============================

.. image:: https://coveralls.io/repos/Starou/django-yaaac/badge.png
  :target: https://coveralls.io/r/Starou/django-yaaac

.. image:: https://img.shields.io/pypi/v/django_yaaac.svg
  :target: https://pypi.python.org/pypi/django-yaaac

.. image:: https://img.shields.io/pypi/pyversions/django_yaaac.svg
    :target: https://pypi.python.org/pypi/django-yaaac/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/django_yaaac.svg
    :target: https://pypi.python.org/pypi/django-yaaac/
    :alt: License

.. image:: https://travis-ci.org/Starou/django-yaaac.svg
    :target: https://travis-ci.org/Starou/django-yaaac
    :alt: Travis C.I.


*Yaaac* is lightweight Django application providing Ajax search to foreign-key form fields.

Version 3 upgrade warning
=========================

This version brings Python 3.6 compatibility with a minor regression.
The default ``suggest_by`` is now ``__str__`` instead of ``__unicode__`` so check
the `Django documentation <https://docs.djangoproject.com/en/1.11/topics/python3/#str-and-unicode-methods>`_
to migrate your code.

Django 2-2 and Version 3.2 important note
=========================================

Since Django-2.2 the way `assets are sorted has been completely rewritten <https://docs.djangoproject.com/en/2.2/releases/2.2/#merging-of-form-media-assets>`_
and as the result breaks this lib in the admin. The fix was to embbed jQuery and set the
dependency in the widgets Media classes which may leads to other regressions.

Since a `autocomplete solution <https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields>`_
is now built-in Django admin, the support for the admin has been removed.


Installation
============

Install the app from the source::

    python setup.py build && (sudo) python setup.py install

Or with *pip*::

    pip install django-yaaac

(for Django < 1.8, use a previous version like ``pip install django-yaaac==1.9.0``)

Add the app in your settings.INSTALLED_APPS:

.. code-block:: python

    INSTALLED_APPS = [
        ...,
        "django_yaaac",
        ...,
    ]

In the *urls.py* module of your project, define the url pattern for ajax calls:

.. code-block:: python

    from django_yaaac.manager import autocomplete
    from django.conf.urls import url

    urlpatterns = [
        ...
        url(r'^yaaac/', autocomplete.urls),
        ...
    ]

Usage
=====

Forms
-----

What you need to do is to declare a custom *ModelForm*:

.. code-block:: python

    from django import forms
    from django.contrib import admin
    from django_yaaac.forms.fields import AutocompleteModelChoiceField
    from . import models


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

        class Media:
            # You need jQuery. Don't forget to call {{ form.media }} in your template.
            js = ('js/jquery.min.js', )


    admin.site.register(models.BandMember, BandMemberAdmin)

The *site* parameter of *AutocompleteModelChoiceField* is required for related lookup (the
magnifier glass). The *search_fields* is a list of fields to search against using the same syntax
as in Django Admin (^, $ etc).
Extra options *min_chars*, *max_height* and *width* are the counter-part of *minChars*, *maxHeight* and *width*
in `Autocomplete options <https://github.com/devbridge/jQuery-Autocomplete#api>`_.

*suggest_by* is optional. It can be a field or a method of the model.
By default, suggestions are shown using *__unicode__* method.

If your model define a ``get_absolute_url()`` method, the label is a link to that resource.

Models
------

The ``Yaaac`` class must defines the following:

- ``user_passes_test`` is a class method that takes a user and return True or False.
- ``allows_suggest_by`` is a list of model fields or methods that can used as return value by the search view.

.. code-block:: python

    class BandMember(models.Model):
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

Tuning
======

To ease the DOM manipulation, HTML classes are added to the elements. The most interesting being ``yaaac_<fieldname>``
to the hidden input storing the foreign key value. This is very convenient when you need to add behavior to a whole
set of fields - also those that don't exist when the page is created - sharing the same name.

Use jQuery delegation (i.e. ``$(".foo").on("change", ".yaaac_first_name")``) to place an event on one field for all
the inline forms present in the page or to come (i.e. Click on "Add a new Band Member".)
