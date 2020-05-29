from rest_framework import serializers

from tweets.models import Tweet
from users.models import User
from users.serializers import UserSerializer
from likes.models import Like
from comments.models import Comment
from retweets.models import Retweet
from followers.models import Follower
from savedTweets.models import SavedTweet


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    retweets = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()
    user_follows_me = serializers.SerializerMethodField()
    user_followed_by_me = serializers.SerializerMethodField()
    is_retweeted = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = (
            'id',
            'content',
            'date',
            'user',
            'likes',
            'comments',
            'retweets',
            'is_mine',
            'user_follows_me',
            'user_followed_by_me',
            'is_retweeted',
            'is_liked',
            'is_saved'
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

    def get_user_followed_by_me(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            follows=Follower.objects.filter(userFollowing__exact=obj.user.id,userFollower__exact=user.id)
            return follows.count()>0
        return False    
            

    def get_user_follows_me(self, obj):
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                follows=Follower.objects.filter(userFollowing__exact=user.id,userFollower__exact=obj.user.id)
                return follows.count()>0
            return False   

    def get_is_mine(self, obj):
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                return user.id == obj.user.id
            return False 
    
    def get_is_liked(self, obj):
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                likes=Like.objects.filter(user=user.id,tweet=obj.id)
                return likes.count()>0
            return False 
    
    def get_is_retweeted(self, obj):
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                retweets=Retweet.objects.filter(user=user.id,originalTweet=obj.id)
                return retweets.count()>0
            return False 

    def get_is_saved(self, obj):
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                savedTweets=SavedTweet.objects.filter(user=user.id,tweet=obj.id)
                return savedTweets.count()>0
            return False 

    #Funcion de representacion que realiza un override al serializer
    def to_representation(self, instance): 
        data = super().to_representation(instance)
        request = self.context.get("request")
        data['user'] = UserSerializer(
            User.objects.get(pk=data['user']),context={'request':request}).data
        return data