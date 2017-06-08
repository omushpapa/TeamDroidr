import os

DB_PASS = os.environ['DB_PASS']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'botops',
        'USER': 'teamdroidr',
        'PASSWORD': DB_PASS
    }
}

INSTALLED_APPS = (
    'data',
    )

SECRET_KEY = '63cFWu$$lhT3bVP9U1k1Iv@Jo02SuM'
