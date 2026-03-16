# Real-Time Chat Application

A scalable real-time chat application built with **Django, Django REST Framework, WebSockets (Django Channels), Celery, and Redis**.
The system supports real-time messaging, read receipts, and background notification processing.

---

## 🚀 Features

* Real-time messaging using WebSockets
* JWT based authentication
* Conversation and message management
* Message persistence in database
* WhatsApp-like read receipts

  * Single tick → message delivered
  * Double tick → message read
* Background notifications using Celery
* Redis used as message broker
* Dockerized development environment

---

## 🛠 Tech Stack

Backend:

* Python
* Django
* Django REST Framework

Real-time Communication:

* Django Channels
* WebSockets

Authentication:

* JWT (JSON Web Token)

Background Tasks:

* Celery
* Redis

Containerization:

* Docker
* Docker Compose

---

## 🏗 System Architecture

User → WebSocket → Django Channels
     │
     ▼
Message stored in Database
     │
     ▼
Celery task triggered
     │
     ▼
Redis (Message Broker)
     │
     ▼
Celery Worker → Notification Processing

---

## 📂 Project Structure

chat_project/

manage.py
Dockerfile
docker-compose.yml

chat_project/
    settings.py
    celery.py
    asgi.py

chat/
    models.py
    consumers.py
    tasks.py
    routing.py

users/
    models.py
    serializers.py
    views.py

---

## ⚙️ Installation

Clone the repository:

git clone https://github.com/your-username/chat-app.git

cd chat-app

---

## 🐳 Run with Docker

Build and start containers:

docker compose up --build

Services started:

* Django application
* Redis
* Celery worker

---

## 📡 WebSocket Endpoint

ws://localhost:8000/ws/chat/<conversation_id>/

---

## 🔔 Background Notifications

When a message is sent:

1. Message is stored in the database
2. WebSocket delivers message to receiver
3. Celery task is triggered
4. Redis queues the task
5. Celery worker processes notification

---

## 🔁 Retry Mechanism

Celery tasks use automatic retry with exponential backoff to handle temporary failures like network issues.

---

## 📌 Future Improvements

* Typing indicators
* Online/offline presence
* Push notifications
* Message reactions
* Redis channel layer for production scaling

---

## 👨‍💻 Author

Arjit Shukla
