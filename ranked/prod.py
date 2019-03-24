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
    "https://api.ranked.wtf",
    "wss://api.ranked.wtf",
    "api.ranked.wtf",
    "https://ranked-gg.herokuapp.com",
)
DEBUG = False
CORS_ORIGIN_ALLOW_ALL = True
