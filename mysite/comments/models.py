from django.db import models


class Comment(models.Model):
    content = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False)
    tweet = models.ForeignKey('tweets.Tweet', on_delete=models.CASCADE, null=True, blank=True)
    retweet = models.ForeignKey('retweets.Retweet', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content
