from rest_framework.views import APIView
from player.models import Player
from .R6TabAPI import R6TabAPI
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from ranked.functions import timedelta_now_hours
from ranked.constants import PLAYER_DATA_REFRESH_HOURS
from .serializers import R6TabUserSerializer, SearchPlayerSerializer


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


class SearchUserView(ListAPIView):
    def get_queryset(self):
        query = self.request.GET.get('query')
        return Player.objects.filter(username__icontains=query)

    def get_serializer_context(self):
        region = self.request.GET.get('region')
        return {"region": region}

    serializer_class = SearchPlayerSerializer
