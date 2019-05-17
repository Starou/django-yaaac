import os
from setuptools import setup

# Python 2.7
from io import open

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
    README = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-yaaac',
    version='3.0.1',
    license='BSD Licence',
    author='Stanislas Guerra',
    author_email='stanislas.guerra@gmail.com',
    description='Django application providing Ajax search capabilities.',
    long_description=README,
    url='https://github.com/Starou/django-yaaac',
    project_urls={
        'Source Code': 'https://github.com/Starou/django-yaaac',
        'Issue Tracker': 'https://github.com/Starou/django-yaaac/issues',
    },
    install_requires=['future'],
    packages=[
        'django_yaaac',
        'django_yaaac.forms',
    ],
    package_data={
        'django_yaaac': [
            'static/django_yaaac/css/*.css',
            'static/django_yaaac/js/*.js',
            'static/django_yaaac/img/*.png',
            'static/django_yaaac/img/*.jpg',
            'static/django_yaaac/img/*.gif',
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
