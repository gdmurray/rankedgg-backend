from rest_framework.views import APIView
from player.models import Player
from .R6TabAPI import R6TabAPI
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import R6TabUserSerializer, SearchPlayerSerializer


# Create your views here.
class SearchUsernameView(APIView):
    def get(self, request, username, *args, **kwargs):
        player = Player.objects.filter(username=username).first()
        region = request.GET.get('region')
        try:
            # If cant find the name in db
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
                    metadata = player.fetch_metadata()
            else:
                metadata = player.get_metadata()
                if player.needs_metadata_fetch():
                    metadata = player.fetch_metadata(metadata)
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

    pagination_class = None
    serializer_class = SearchPlayerSerializer
