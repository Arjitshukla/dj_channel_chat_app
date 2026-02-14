from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """
    Represents a chat room (1-to-1 or group)
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations"
    )
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Stores individual messages inside a conversation
    """
    MESSAGE_TYPE_CHOICES = (
        ("text", "Text"),
        ("image", "Image"),
        ("file", "File"),
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    content = models.TextField()
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
        default="text"
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender}"


class MessageReadStatus(models.Model):
    """
    Tracks which user has read which message
    (Scalable for group chat)
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="read_status"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("message", "user")

    def __str__(self):
        return f"{self.user} read {self.message}"


class Notification(models.Model):
    """
    Stores notifications (message alerts etc.)
    """
    NOTIFICATION_TYPE_CHOICES = (
        ("message", "Message"),
        ("system", "System"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
        default="message"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"
