from django.db import models


class Message(models.Model):
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False, related_name='sender')
    receiver = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False, related_name='receiver')
    
    def __str__(self):
        return self.content
