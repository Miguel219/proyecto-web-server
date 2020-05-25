from django.db import models


class Chat(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
