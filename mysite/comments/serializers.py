from rest_framework import serializers

from comments.models import Comment
from users.serializers import UserSerializer
from tweets.serializers import TweetSerializer
from retweets.serializers import RetweetSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    tweet = TweetSerializer()
    retweet = RetweetSerializer()
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'date',
            'user',
            'tweet',
            'retweet'
        )
