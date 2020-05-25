from rest_framework import serializers

from retweets.models import Retweet
from users.models import User
from users.serializers import UserSerializer
from tweets.models import Tweet
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

    #Funcion de representacion que realiza un override al serializer
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['originalTweet'] = TweetSerializer(
            Tweet.objects.get(pk=data['originalTweet'])).data
        data['user'] = UserSerializer(
            User.objects.get(pk=data['user'])).data
        return data
