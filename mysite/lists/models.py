from django.db import models


class List(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return self.content
