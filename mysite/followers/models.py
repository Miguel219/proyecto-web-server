from django.db import models


class Follower(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    userFollower = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False, related_name='userFollower')
    userFollowing = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False, related_name='userFollowing')
    
    def __str__(self):
        return str(self.id)
