from .settings import *

import dj_database_url
ALLOWED_HOSTS = [
    "ranked-gg.herokuapp.com",
    "ranked.wtf"
]

CORS_ORIGIN_WHITELIST = (
    'ranked.wtf'
)

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)