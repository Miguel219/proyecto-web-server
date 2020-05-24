from rest_framework import serializers

from savedTweets.models import SavedTweet
from tweets.serializers import TweetSerializer
from retweets.serializers import RetweetSerializer
from users.serializers import UserSerializer

class SavedTweetSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer()
    retweet = RetweetSerializer()
    user = UserSerializer()

    class Meta:
        model = SavedTweet
        fields = (
            'id',
            'date',
            'tweet',
            'retweet',
            'user'
        )
        