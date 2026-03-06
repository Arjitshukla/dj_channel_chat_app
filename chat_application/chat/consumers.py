import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
from chat.models import Conversation, Message, MessageReadStatus


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        # join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # unread messages mark as read when user opens chat
        await self.mark_all_as_read()

        await self.send(text_data=json.dumps({
            "type": "connection",
            "message": "Connected",
            "user": self.user.username
        }))

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        message_type = data.get("type", "message")

        # SEND MESSAGE
        if message_type == "message":

            message_text = data.get("message")

            message_id = await self.save_message(message_text)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_text,
                    "message_id": message_id,
                    "sender": self.user.username
                }
            )

        # READ EVENT
        if message_type == "read":

            message_id = data.get("message_id")

            sender = await self.mark_as_read(message_id)

            # send read event ONLY to sender
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "message_read",
                    "message_id": message_id,
                    "reader": self.user.username,
                    "sender": sender
                }
            )

    # RECEIVE MESSAGE
    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"],
            "message_id": event["message_id"],
            "sender": event["sender"]
        }))

    # RECEIVE READ EVENT
    async def message_read(self, event):

        # only sender should see blue tick
        if event["sender"] == self.user.username:

            await self.send(text_data=json.dumps({
                "type": "read",
                "message_id": event["message_id"],
                "user": event["reader"]
            }))

#  DATABASE FUNCTIONS 

    @sync_to_async
    def save_message(self, message_text):

        conversation = Conversation.objects.get(id=self.conversation_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=message_text
        )

        # create delivered status
        for user in conversation.participants.all():

            if user != self.user:

                MessageReadStatus.objects.get_or_create(
                    message=message,
                    user=user
                )

        return message.id


    @sync_to_async
    def mark_as_read(self, message_id):

        try:

            read_status = MessageReadStatus.objects.get(
                message_id=message_id,
                user=self.user
            )

            read_status.is_read = True
            read_status.read_at = timezone.now()
            read_status.save()

            message = Message.objects.get(id=message_id)

            return message.sender.username

        except MessageReadStatus.DoesNotExist:
            return None


    @sync_to_async
    def mark_all_as_read(self):

        unread = MessageReadStatus.objects.filter(
            user=self.user,
            is_read=False
        )

        for item in unread:

            item.is_read = True
            item.read_at = timezone.now()
            item.save()