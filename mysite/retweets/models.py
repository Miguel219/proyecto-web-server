from django.db import models


class Retweet(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False, related_name='user')
    originalTweet = models.ForeignKey('tweets.Tweet', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.originalTweet
