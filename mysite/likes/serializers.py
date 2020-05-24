from rest_framework import serializers

from likes.models import Like
from users.serializers import UserSerializer
from tweets.serializers import TweetSerializer
from retweets.serializers import RetweetSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    tweet = TweetSerializer()
    retweet = RetweetSerializer()
    
    class Meta:
        model = Like
        fields = (
            'id',
            'date',
            'user',
            'tweet',
            'retweet'
        )
