from rest_framework import serializers

from comments.models import Comment
from users.models import User
from users.serializers import UserSerializer
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from retweets.models import Retweet
from retweets.serializers import RetweetSerializer


class CommentSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'date',
            'user',
            'tweet',
            'retweet',
            'is_mine',
        )

    def get_is_mine(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return user.id == obj.user.id
        return False 

    #Funcion de representacion que realiza un override al serializer
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        data['user'] = UserSerializer(
            User.objects.get(pk=data['user']),context={'request':request}).data
        if(data['tweet']):
            data['tweet'] = TweetSerializer(
                Tweet.objects.get(pk=data['tweet']),context={'request':request}).data
        if(data['retweet']):
            data['retweet'] = RetweetSerializer(
                Retweet.objects.get(pk=data['retweet']),context={'request':request}).data
        return data