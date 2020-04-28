from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chatting, Chatting_room
import json
from django.core import serializers

class ChatConsumer(AsyncWebsocketConsumer):
  async def init_chat(self, data):
    self.room_id = data['room_id']
    content = { 'command': 'init_chat' }
    
    try:
      room = Chatting_room.objects.get(id=self.room_id)
    except:
      pass

    # Join room group
    await self.channel_layer.group_add(self.room_id, self.channel_name)

    if not room:
      content['error'] = 'Unable to get or create Chatting Room'
      self.send_message(content)

    content['success'] = 'Success with get or create Chatting Room'
    self.position = data['position']

  async def fetch_messages(self, data):
    try:
      chatting = Chatting_room.objects.get(id=self.room_id).chatting_set.all()
    except:
      chatting = {}

    content = {
      'command': 'fetch_messages',
      'messages': self.chattings_to_json(chatting)
    }
    await self.send_message(content)

  async def new_message(self, data):
    position, message = data['position'], data['message']
    room = Chatting_room.objects.get(id=self.room_id)
    lawyer, author = room.lawyer, room.author

    try:
      if position == "lawyer":
        chatting = Chatting.objects.create(author=None, lawyer=lawyer, room=room, content=message)
      else:
        chatting = Chatting.objects.create(author=author, lawyer=None, room=room, content=message)
    except:
      print("new_message : Error")
      return

    content = {
        'command': 'new_message',
        'message': self.chatting_to_json(chatting)
    }
    await self.send_chat_message(content)

  commands = {
    'init_chat': init_chat,
    'fetch_messages': fetch_messages,
    'new_message': new_message
  }

  def chattings_to_json(self, chattings):
    result = {}
    for index, chatting in enumerate(chattings):
      result.setdefault(index, self.chatting_to_json(chatting))
    return result

  def chatting_to_json(self, chatting):
    return {
      'author': chatting.author.name if chatting.author else "",
      'lawyer': chatting.lawyer.name if chatting.lawyer else "",
      'content': chatting.content,
      'pub_date': chatting.pub_date.strftime('%m.%d %p %I:%M'),
    }
  # websocket이 연결 되었을 때 행해질 메서드
  async def connect(self):
    await self.accept()
  # 연결이 끊길 경우 행해질 메서드
  async def disconnect(self):
    # leave group room
    await self.channel_layer.group_discard(self.room_id, self.channel_name)
  # 클라이언트로부터 메세지를 받으면 행해질 메서드
  async def receive(self, text_data):
    data = json.loads(text_data)
    print(data)
    await self.commands[data['command']](self, data)

  async def send_message(self, message):
    await self.send(text_data=json.dumps(message))

  async def send_chat_message(self, message):
    # Send message to room group
    await self.channel_layer.group_send(self.room_id, { 'type': 'chat_message', 'message': message })

  # Receive message from room group
  async def chat_message(self, event):
    message = event['message']
    # Send message to WebSocket
    await self.send(text_data=json.dumps(message))
