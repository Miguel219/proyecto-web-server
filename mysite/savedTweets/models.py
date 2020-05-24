from django.db import models


class SavedTweet(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    tweet = models.ForeignKey('tweets.Tweet', on_delete=models.CASCADE, null=True, blank=True)
    retweet = models.ForeignKey('retweets.Retweet', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return self.content
