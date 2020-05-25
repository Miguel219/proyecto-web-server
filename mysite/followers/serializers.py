from rest_framework import serializers

from followers.models import Follower
from users.models import User
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
        
    #Funcion de representacion que realiza un override al serializer
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['userFollower'] = UserSerializer(
            User.objects.get(pk=data['userFollower'])).data
        data['userFollowing'] = UserSerializer(
            User.objects.get(pk=data['userFollowing'])).data
        return data