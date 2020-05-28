from rest_framework import serializers

from users.models import User
from followers.models import Follower

#Clase User Serializer
class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    im_following = serializers.SerializerMethodField()
    they_follow = serializers.SerializerMethodField()
    is_me = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'followers',
            'following',
            'date_joined',
            'last_login',
            'im_following',
            'they_follow',
            'is_me',
        )

    def get_followers(self, obj):
        followers = Follower.objects.filter(userFollowing=obj.id)
        return followers.count()

    def get_following(self, obj):
        following = Follower.objects.filter(userFollower=obj.id)
        return following.count()


    def get_im_following(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            follows=Follower.objects.filter(userFollowing__exact=obj.id,userFollower__exact=user.id)
            return follows.count()>0
        return False    
            

    def get_they_follow(self, obj):
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                follows=Follower.objects.filter(userFollowing__exact=user.id,userFollower__exact=obj.id)
                return follows.count()>0
            return False   

    def get_is_me(self, obj):
            user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                return user.id == obj.id
            return False 
