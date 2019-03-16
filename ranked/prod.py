from .settings import *

ALLOWED_HOSTS = [
    "ranked-gg.herokuapp.com",
    "ranked.wtf"
]

CORS_ORIGIN_WHITELIST = (
    'ranked.wtf',
    'http://ranked.wtf',
    'https://www.ranked.wtf',
    "ranked-gg.herokuapp.com",
    "https://ranked-gg.herokuapp.com",
)
