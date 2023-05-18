# voice_call_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'call_%s' % self.room_name

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        if message_type == 'call':
            recipient = text_data_json['recipient']

            # Send the call notification to the recipient
            await self.channel_layer.group_send(
                'call_%s' % recipient,
                {
                    'type': 'call_notification',
                    'caller': self.room_name
                }
            )
        elif message_type == 'accept':
            caller = text_data_json['caller']

            # Send the call acceptance to the caller
            await self.channel_layer.group_send(
                'call_%s' % caller,
                {
                    'type': 'call_acceptance',
                    'recipient': self.room_name
                }
            )
        elif message_type == 'reject':
            caller = text_data_json['caller']

            # Send the call rejection to the caller
            await self.channel_layer.group_send(
                'call_%s' % caller,
                {
                    'type': 'call_rejection',
                    'recipient': self.room_name
                }
            )

    async def call_notification(self, event):
        caller = event['caller']

        # Send the call notification to the client
        await self.send(text_data=json.dumps({
            'type': 'call_notification',
            'caller': caller
        }))

    async def call_acceptance(self, event):
        recipient = event['recipient']

        # Send the call acceptance to the client
        await self.send(text_data=json.dumps({
            'type': 'call_acceptance',
            'recipient': recipient
        }))

    async def call_rejection(self, event):
        recipient = event['recipient']

        # Send the call rejection to the client
        await self.send(text_data=json.dumps({
            'type': 'call_rejection',
            'recipient': recipient
        }))
