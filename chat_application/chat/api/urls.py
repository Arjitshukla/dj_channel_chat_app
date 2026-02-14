from django.urls import path
from .views import *

urlpatterns = [
    path("conversations/", MyConversationsView.as_view()),
    path("conversations/create/", CreateConversationView.as_view()),
    path("messages/send/", SendMessageView.as_view()),
    path("conversations/<int:conversation_id>/messages/", ConversationMessagesView.as_view()),
]
