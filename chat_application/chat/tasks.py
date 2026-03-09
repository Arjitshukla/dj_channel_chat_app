from celery import shared_task
from chat.models import Message

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_message_notification(message_id):
    '''
    Celery task to send notifications when a new message is sent.
    '''

    message = Message.objects.get(id=message_id)
    sender = message.sender.username

    receivers = message.conversation.participants.exclude(
        id=message.sender.id
    )

    for user in receivers:
        print(f"Notification -> {user.username}: {sender} sent a message")