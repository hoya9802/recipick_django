from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    shop_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shop_chatrooms'
    )
    visitor_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='visitor_chatrooms'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('shop_user', 'visitor_user')


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE,
        related_name="messages"
    )
    sender_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='sent_messages'
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
