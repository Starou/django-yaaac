#!/usr/bin/env python
#
# Inspired from https://github.com/django/django/blob/master/tests/runtests.py.
#
from argparse import ArgumentParser
import os
import sys

import django
from django import contrib
from django.apps import apps
from django.conf import settings
from django.db import connection
from django.test import TestCase
from django.test.utils import get_runner
from django.utils._os import upath


TEST_TEMPLATE_DIR = 'templates'

RUNTESTS_DIR = os.path.abspath(os.path.dirname(upath(__file__)))

SUBDIRS_TO_SKIP = [
    'data',
]

ALWAYS_INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_yaaac',
]

ALWAYS_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


def get_test_modules():
    modules = []
    for f in os.listdir(RUNTESTS_DIR):
        if ('.' in f or
                f.startswith('sql') or
                os.path.basename(f) in SUBDIRS_TO_SKIP or
                os.path.isfile(f) or
                not os.path.exists(os.path.join(f, '__init__.py'))):
            continue
        modules.append(f)
    return modules


def get_installed():
    return [app_config.name for app_config in apps.get_app_configs()]


def setup(verbosity, test_labels):
    state = {
        'INSTALLED_APPS': settings.INSTALLED_APPS,
        'ROOT_URLCONF': getattr(settings, "ROOT_URLCONF", ""),
        'TEMPLATE_DIRS': settings.TEMPLATE_DIRS,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_ROOT': settings.STATIC_ROOT,
        'MIDDLEWARE_CLASSES': settings.MIDDLEWARE_CLASSES,
    }

    # Redirect some settings for the duration of these tests.
    settings.INSTALLED_APPS = ALWAYS_INSTALLED_APPS
    settings.ROOT_URLCONF = 'urls'
    settings.STATIC_URL = '/static/'
    settings.STATIC_ROOT = ''
    settings.TEMPLATE_DIRS = (os.path.join(RUNTESTS_DIR, TEST_TEMPLATE_DIR),)
    settings.LANGUAGE_CODE = 'en'
    settings.SITE_ID = 1
    settings.MIDDLEWARE_CLASSES = ALWAYS_MIDDLEWARE_CLASSES
    # Ensure the middleware classes are seen as overridden otherwise we get a compatibility warning.
    settings._explicit_settings.add('MIDDLEWARE_CLASSES')
    settings.MIGRATION_MODULES = {
        # these 'tests.migrations' modules don't actually exist, but this lets
        # us skip creating migrations for the test models.
        'auth': 'django.contrib.auth.tests.migrations',
        'contenttypes': 'django.contrib.contenttypes.tests.migrations',
    }

    # Load all the ALWAYS_INSTALLED_APPS.
    django.setup()

    # Load the test model apps.
    if not test_labels:
        modules = get_test_modules()
    else:
        modules = set([label.split(".")[0] for label in test_labels])

    for module_label in modules:
        settings.INSTALLED_APPS.append(module_label)
    apps.set_installed_apps(settings.INSTALLED_APPS)

    return state


def teardown(state):
    # Restore the old settings.
    for key, value in state.items():
        setattr(settings, key, value)


def django_tests(verbosity, test_labels):
    state = setup(verbosity, test_labels)

    if not hasattr(settings, 'TEST_RUNNER'):
        settings.TEST_RUNNER = 'django.test.runner.DiscoverRunner'
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity)
    failures = test_runner.run_tests(test_labels or get_test_modules())

    teardown(state)
    return failures


if __name__ == "__main__":
    parser = ArgumentParser(description="Run the Django test suite.")
    parser.add_argument('modules', nargs='*', metavar='module',
        help='Optional path(s) to test modules; e.g. "i18n" or '
             '"i18n.tests.TranslationTests.test_lazy_objects".')
    parser.add_argument(
        '-v', '--verbosity', default=1, type=int, choices=[0, 1, 2, 3],
        help='Verbosity level; 0=minimal output, 1=normal output, 2=all output')
    parser.add_argument('--liveserver',
        help='Overrides the default address where the live server (used with '
             'LiveServerTestCase) is expected to run from. The default value '
             'is localhost:8081.')
    parser.add_argument(
        '--selenium', action='store_true', dest='selenium', default=False,
        help='Run the Selenium tests as well (if Selenium is installed)')
    options = parser.parse_args()

    # Allow including a trailing slash on app_labels for tab completion convenience
    options.modules = [os.path.normpath(labels) for labels in options.modules]

    if options.liveserver is not None:
        os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = options.liveserver

    if options.selenium:
        os.environ['DJANGO_SELENIUM_TESTS'] = '1'

    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_sqlite_settings'
    failures = django_tests(options.verbosity, options.modules)
    if failures:
        sys.exit(bool(failures))
