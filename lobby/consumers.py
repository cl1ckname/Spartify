import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class LobbyConsumer(AsyncWebsocketConsumer):
    ''' Consumer to communicate with the lobby page via WebSocket '''
    async def connect(self):
        ''' Add layer to group on new connection '''
        self.lobby_id = self.scope['url_route']['kwargs']['int']
        self.group_name = "lobby_"+self.lobby_id
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    
    async def receive(self, text_data):
        print('recived', text_data)


    async def disconnect(self, code):
        ''' Remove layer from group on disconnect'''
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def ban(self, event):
        print(event)
        await self.send(text_data=json.dumps({'type': 'websocket.send', 'username': event['username'], 'userid': event['userid']}))

    async def unban(self, event):
        print(event)
        await self.send(text_data=json.dumps({'type': 'websocket.send', 'unbanned': event['unbanned']}))