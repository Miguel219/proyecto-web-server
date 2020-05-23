from rest_framework import serializers

from savedTweets.models import SavedTweet
from tweets.serializers import TweetSerializer
from users.serializers import UserSerializer

class SavedTweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedTweet
        fields = (
            'id',
            'date',
            'tweet',
            'user'
        )
        