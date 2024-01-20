import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Add the new connection to the group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection
        self.accept()
        print("Connection established.")

        # Load previous messages and send them to the connected client
        self.send_previous_messages()

    def disconnect(self, close_code):
        # Remove the connection from the group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json['username']

        # Save the received message to the database
        Message.objects.create(room_name=self.room_name, username=username, content=message)

        # Broadcast the received message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, "username": username}
        )

    def chat_message(self, event):
        # Send the message to the WebSocket
        self.send(text_data=json.dumps(event))

    def send_previous_messages(self):
        # Retrieve previous messages from the database
        previous_messages = Message.objects.filter(room_name=self.room_name).order_by('-timestamp')[:100]

        # Send the previous messages to the connected client
        for message in reversed(previous_messages):
            self.send(text_data=json.dumps({
                'type': 'chat.message',
                'message': message.content,
                'username': message.username
            }))