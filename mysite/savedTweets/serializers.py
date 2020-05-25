from rest_framework import serializers

from savedTweets.models import SavedTweet
from users.models import User
from users.serializers import UserSerializer
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from retweets.models import Retweet
from retweets.serializers import RetweetSerializer

class SavedTweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedTweet
        fields = (
            'id',
            'date',
            'tweet',
            'retweet',
            'user'
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