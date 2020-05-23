from rest_framework import serializers

from followers.models import Follower
from users.serializers import UserSerializer

class FollowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = (
            'id',
            'date',
            'userFollower',
            'userFollowing'
        )
        