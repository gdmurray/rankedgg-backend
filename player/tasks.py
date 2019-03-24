from ranked.celery import app
from .models import Player

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@app.task
def update_ranked_data(pk, region=None):
    player = Player.objects.get(id=pk)
    print(f"Updating Ranked Data for {player.username}")
    metadata, updated_player = player.fetch_metadata(include_player=True)
    from .serializers import PlayerLeaderBoardSerializer
    serializer = PlayerLeaderBoardSerializer(updated_player, many=False,
                                             context={"region": region, "from_task": True}).data

    layer = get_channel_layer()
    async_to_sync(layer.group_send)('updates', {
        'type': 'player_updates',
        'content': serializer
    })
