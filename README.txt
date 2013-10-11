===============================
Another Ajax Auto-Complete, Yet
===============================

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
                                                "value_attr": "name"
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
magnifier glass). The *value_attr* is the model attribute used for the suggestions.

Do not forget to add *jQuery* in your template (using *ModelAdmin.Media.js* in the example above).
Outside the admin, you have to explicitly call the yaaac static files like that::
    
    <head>
      {{ form.media }}
    </head>
