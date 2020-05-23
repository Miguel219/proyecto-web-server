from django.db import models


class ListUser(models.Model):
    list = models.ForeignKey('lists.List', on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return self.date
