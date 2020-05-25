from rest_framework import serializers

from likes.models import Like
from users.models import User
from users.serializers import UserSerializer
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from retweets.models import Retweet
from retweets.serializers import RetweetSerializer


class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = (
            'id',
            'date',
            'user',
            'tweet',
            'retweet'
        )

    #Funcion de representacion que realiza un override al serializer
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(
            User.objects.get(pk=data['user'])).data
        if(data['tweet']):
            data['tweet'] = TweetSerializer(
                Tweet.objects.get(pk=data['tweet'])).data
        if(data['retweet']):
            data['retweet'] = RetweetSerializer(
                Retweet.objects.get(pk=data['retweet'])).data
        return data