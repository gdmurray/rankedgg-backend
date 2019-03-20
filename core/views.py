from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Player, PlayerMeta, Report
from operators.models import Operator
from .serializers import R6TabUserSerializer, SearchPlayerSerializer
from rest_framework.response import Response
from .R6TabAPI import R6TabAPI
from ipware import get_client_ip
from ranked.constants import PLAYER_DATA_REFRESH_HOURS, METADATA_REFRESH_HOURS, ATTACKER, DEFENDER
from .functions import timedelta_now_hours
from django.db.models import Count
from operators.serializers import OperatorSelectSerializer


# Create your views here.


class SearchUsernameView(APIView):
    def get(self, request, username, *args, **kwargs):
        player = Player.objects.filter(username=username).first()
        region = request.GET.get('region')
        try:
            if not player:
                try:
                    user_data = R6TabAPI.find_by_username(username)
                    if not user_data:
                        return Response(status=404)
                except KeyError:
                    return Response(status=404)
                else:
                    player_id = user_data['p_id']
                    player, created = Player.objects.get_or_create(p_id=player_id)
                    R6TabAPI.save_defaults(player, user_data)
            else:
                if timedelta_now_hours(player.last_queried) > PLAYER_DATA_REFRESH_HOURS:
                    print("Player Refresh Time")
                    user_data = R6TabAPI.find_by_username(username)
                    R6TabAPI.save_defaults(player, user_data)
            metadata = player.fetch_metadata()
            data = R6TabUserSerializer(player, many=False, context={"region": region, "metadata": metadata}).data
            return Response(data=data, status=200)

        except Exception as e:
            print("Exception ", e)
            return Response(status=500)


class ReportUserView(APIView):
    # TODO: ADD IP ENFORCEMENT ON WEBSITE
    def post(self, request, *args, **kwargs):
        client_ip, is_routable = get_client_ip(request)
        player = Player.objects.filter(username=request.data['username']).first()
        operator = Operator.objects.filter(name=request.data['operator'].capitalize()).first()
        if player and operator:
            report = Report.objects.create(
                sender_ip=client_ip,
                player=player,
                operator=operator,
                region=request.data['region']
            )
            return Response(status=200)
        else:
            return Response(status=404)


class SearchUserView(ListAPIView):
    def get_queryset(self):
        query = self.request.GET.get('query')
        return Player.objects.filter(username__icontains=query)

    def get_serializer_context(self):
        region = self.request.GET.get('region')
        return {"region": region}

    serializer_class = SearchPlayerSerializer


class MostReportedOperators(APIView):
    def get(self, request, *args, **kwargs):
        region = request.GET.get("region")
        if region:
            attackers = Report.objects.filter(operator__type=ATTACKER, region=region).values_list('operator').annotate(
                report_count=Count('operator')).order_by('-report_count')
            defenders = Report.objects.filter(operator__type=DEFENDER, region=region).values_list('operator').annotate(
                report_count=Count('operator')).order_by('-report_count')
        else:
            attackers = Report.objects.filter(operator__type=ATTACKER).values_list('operator').annotate(
                report_count=Count('operator')).order_by('-report_count')
            defenders = Report.objects.filter(operator__type=DEFENDER).values_list('operator').annotate(
                report_count=Count('operator')).order_by('-report_count')

        data = {
            "attacker": None,
            "defender": None
        }
        print(attackers)
        print(defenders)
        if attackers.count() >= 1:
            top_atk_id = attackers[0][0]
            top_atk_rate = attackers[0][1]

            attacker = Operator.objects.get(id=top_atk_id)
            data["attacker"] = {
                "rate": top_atk_rate,
                "operator": OperatorSelectSerializer(attacker, many=False).data
            }

        if defenders.count() >= 1:
            top_def_id = defenders[0][0]
            top_def_rate = defenders[0][1]

            defender = Operator.objects.get(id=top_def_id)
            data["defender"] = {
                "rate": top_def_rate,
                "operator": OperatorSelectSerializer(defender, many=False).data
            }

        return Response(data=data, status=200)


class MostNotoriousPlayers(APIView):
    def get(self, request, operator, *args, **kwargs):
        region = request.GET.get("region")
        operator = operator.capitalize()
        op_obj = Operator.objects.filter(name=operator).first()
        print("OP id ", op_obj.id)
        if region:
            query = Report.objects.filter(operator_id=op_obj.id, region=region)
        else:
            query = Report.objects.filter(operator_id=op_obj.id)
        players = query.values_list('player_id',
                                    'player__username',
                                    'operator_id').annotate(
            report_count=Count('operator')).order_by('-report_count')[0:10]
        player_list = [{"user_id": p[0], "username": p[1], "reports": p[3]} for p in players]
        return Response(data=player_list, status=200)
