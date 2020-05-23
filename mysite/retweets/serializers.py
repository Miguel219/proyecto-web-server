from rest_framework import serializers

from retweets.models import Retweet
from users.serializers import UserSerializer
from tweets.serializers import TweetSerializer
from likes.models import Like
from comments.models import Comment


class RetweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Retweet
        fields = (
            'id',
            'date',
            'content',
            'user',
            'originalUser',
            'originalTweet',
            'likes',
            'comments'
        )

    def get_likes(self, obj):
        likes = Like.objects.filter(retweet=obj.id)
        return likes.count()

    def get_comments(self, obj):
        comments = Comment.objects.filter(retweet=obj.id)
        return comments.count()
