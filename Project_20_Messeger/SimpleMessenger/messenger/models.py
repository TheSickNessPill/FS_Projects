from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    text = models.TextField(editable=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)


class Dialog(models.Model):
    id_number = models.IntegerField(editable=False)
    member = models.ForeignKey(User, on_delete=models.CASCADE)


class Chat(models.Model):
    chat_name = models.CharField(max_length=50, editable=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    is_creater  = models.BooleanField(editable=True)


class DialogMessages(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)


class ChatMessages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
