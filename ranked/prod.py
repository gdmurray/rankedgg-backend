from .settings import *

ALLOWED_HOSTS = [
    'backend',
    'daphne',
    'api.ranked.wtf',
    "ranked.wtf"
]

CORS_ORIGIN_WHITELIST = (
    'ranked.wtf',
    'http://ranked.wtf',
    'https://www.ranked.wtf',
    "ranked-gg.herokuapp.com",
    "https://ranked-gg.herokuapp.com",
)
DEBUG = False
CORS_ORIGIN_ALLOW_ALL = True
