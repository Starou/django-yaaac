import os
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(CURRENT_DIR, 'database.db'),
        'TEST': {
            'NAME': os.path.join(CURRENT_DIR, 'test_database.db'),
        }
    },
}
SECRET_KEY = 'i0_+-t@@wul&q)30+4y)8-19s)31@%cv8$q(c@8q1g#h$6wn-='
USE_TZ = True
