from rest_framework import serializers

from users.models import User
from followers.models import Follower

#Clase User Serializer
class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

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
            'last_login'
        )

    def get_followers(self, obj):
        followers = Follower.objects.filter(userFollowing=obj.id)
        return followers.count()

    def get_following(self, obj):
        following = Follower.objects.filter(userFollower=obj.id)
        return following.count()