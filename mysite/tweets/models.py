from django.db import models


class Tweet(models.Model):
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return self.content
