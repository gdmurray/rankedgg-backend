from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Player, PlayerMeta, Report
from operators.models import Operator
from .serializers import R6TabUserSerializer, \
    SearchPlayerSerializer, PlayerLeaderBoardSerializer, StandardResultsSetPagination
from rest_framework.response import Response
from .R6TabAPI import R6TabAPI
from ipware import get_client_ip
from ranked.constants import PLAYER_DATA_REFRESH_HOURS, METADATA_REFRESH_HOURS, ATTACKER, DEFENDER
from .functions import timedelta_now_hours
from django.db.models import Count, Q
from operators.serializers import OperatorSelectSerializer
from django.db.models import Sum, F
from django.db.models.expressions import Window
from django.db.models.functions import Rank, RowNumber
from rest_framework.pagination import PageNumberPagination


# Create your views here.





