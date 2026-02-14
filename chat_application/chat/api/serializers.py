from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Conversation, Message

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class MessageSerializer(serializers.ModelSerializer):
    sender = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender",
            "content",
            "message_type",
            "created_at",
        ]
        read_only_fields = ["sender", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = SimpleUserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source="participants"
    )

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "participant_ids",
            "is_group",
            "created_at",
        ]
        read_only_fields = ["created_at"]
