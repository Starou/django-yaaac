===============================
Another Ajax Auto-Complete, Yet
===============================

*Yaaac* is lightweight Django application providing Ajax search to fill foreign key fields in forms (admin or not).

..image:: examples/screenshot-1.png


Installation
============

Install the app from the source::

    python setup.py build && (sudo) python setup.py install

Or with *pip*::

    #TODO

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
