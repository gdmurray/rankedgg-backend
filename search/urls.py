from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    url(r'r6tab/username/(?P<username>.*)', SearchUsernameView.as_view(), name='dropdown-operator-list'),
    url(r'search', SearchUserView.as_view(), name="search-user"),
]
