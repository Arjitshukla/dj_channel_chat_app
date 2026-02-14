from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from ..models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class CreateConversationView(generics.CreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MyConversationsView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).distinct()


class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]

        if self.request.user not in conversation.participants.all():
            raise PermissionError("You are not part of this conversation.")

        serializer.save(sender=self.request.user)


class ConversationMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs["conversation_id"]
        return Message.objects.filter(
            conversation_id=conversation_id
        ).order_by("created_at")
