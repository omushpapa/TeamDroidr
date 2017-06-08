import os
import dj_database_url

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

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
