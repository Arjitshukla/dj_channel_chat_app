from django.shortcuts import render

def login_page(request):
    return render(request, "login.html")

def conversations_page(request):
    return render(request, "conversations.html")

def chat_page(request, conversation_id):
    return render(request, "chat.html", {
        "conversation_id": conversation_id
    })