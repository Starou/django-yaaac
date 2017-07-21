import os
from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-yaaac',
    version='1.11.0',
    license='BSD Licence',
    author='Stanislas Guerra',
    author_email='stanislas.guerra@gmail.com',
    description='Django application providing Ajax search capabilities.',
    long_description=README,
    url='https://github.com/Starou/django-yaaac',
    packages=['django_yaaac',
              'django_yaaac.forms'],
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
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
