from django.urls import path
from .views import login_page, conversations_page, chat_page

urlpatterns = [
    path("", login_page, name="login"),
    path("conversations/", conversations_page, name="conversations"),
    path("chat/<int:conversation_id>/", chat_page, name="chat"),
]