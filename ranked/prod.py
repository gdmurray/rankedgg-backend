from .settings import *

import dj_database_url

ALLOWED_HOSTS = [
    "ranked-gg.herokuapp.com",
    "ranked.wtf"
]

CORS_ORIGIN_WHITELIST = (
    'ranked.wtf'
)
print(os.environ.get('DATABASE_URL'))
DATABASES['default'] = dj_database_url.config()
# DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
