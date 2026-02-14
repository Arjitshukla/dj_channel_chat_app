from django.contrib import admin
from .models import Conversation, Message, MessageReadStatus ,Notification

# Register your models here.
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "is_group", "created_at")
    filter_horizontal = ("participants",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "message_type", "created_at")
    list_filter = ("message_type", "created_at")

@admin.register(MessageReadStatus)
class MessageReadStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "user", "is_read")
    list_filter = ("is_read",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "is_seen", "created_at")
    list_filter = ("is_seen", "created_at")
