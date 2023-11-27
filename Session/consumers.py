from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import jwt
from .models import Session
from django.conf import settings

class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]        
        self.session =  f"session_{self.session_id}"        
        await self.accept()
    
    async def disconnect(self,close_code):        
        await self.channel_layer.group_discard(self.session, self.channel_name)
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)                
        if 'access' not in text_data_json:
            await self.close(code=4001)
        try:
            if self.profile:
                print(self.profile)
        except Exception as e:            
                print(e)    
                decoded = await self.get_user(text_data_json['access'])
                self.profile = decoded['profile']
                print(self.profile)
        if self.profile.role == 'teacher':
            get_session = await self.get_session(self.session_id)
                        
        else:
            pass
        await self.channel_layer.group_add(self.session, self.channel_name)

        # Send message to room group
        message='{"data":"hello"}'
        await self.channel_layer.group_send(
            self.session, {"type": "chat.message", "message": message}
        )    

    @database_sync_to_async
    def get_session(self,session_id):
        session_obj = Session.objects.get(session_id=session_id)
        return session_obj
    
    @database_sync_to_async
    def get_user(self,token):
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded
    
    async def chat_message(self, event):        
        message = event["message"]
        if self.profile['role'] == 'student':
            await self.send(text_data=json.dumps({"message": message}))
