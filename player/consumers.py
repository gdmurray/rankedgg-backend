from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json


class SearchResultUpdateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'updates',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print("Closed websocket with code: ", close_code)
        await self.channel_layer.group_discard(
            'updates',
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        print("Received event: {}".format(content))

        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        """
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        """

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def player_updates(self, event):
        await self.send_json({
            'type': 'player.updates',
            'content': event['content']
        })
