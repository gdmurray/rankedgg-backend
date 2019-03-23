from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    url(r'r6tab/username/(?P<username>.*)', SearchUsernameView.as_view(), name='dropdown-operator-list'),
    url(r'report/submit/', ReportUserView.as_view(), name='report-user'),
    url(r'search', SearchUserView.as_view(), name="search-user"),
    url(r'home/top_operators', MostReportedOperators.as_view(), name="top-reported-operators"),
    url(r'home/notorious/(?P<operator>.*)', MostNotoriousPlayers.as_view(), name="most-notorious-players"),
    url(r'leaderboard/', PlayerLeaderBoardView.as_view(), name="player-leader-board-view")
    # url(r'^api/', include('operators.urls', namespace='operators')),
]
