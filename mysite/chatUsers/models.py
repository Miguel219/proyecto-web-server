from django.db import models


class ChatUser(models.Model):
    chat = models.ForeignKey('chats.Chat', on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return str(self.id)
