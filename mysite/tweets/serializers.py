from rest_framework import serializers

from tweets.models import Tweet
from users.serializers import UserSerializer
from likes.models import Like
from comments.models import Comment
from retweets.models import Retweet


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    retweets = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = (
            'id',
            'content',
            'date',
            'user',
            'likes',
            'comments',
            'retweets'
        )

    def get_likes(self, obj):
        likes = Like.objects.filter(tweet=obj.id)
        return likes.count()

    def get_comments(self, obj):
        comments = Comment.objects.filter(tweet=obj.id)
        return comments.count()

    def get_retweets(self, obj):
        retweets = Retweet.objects.filter(originalTweet=obj.id)
        return retweets.count()