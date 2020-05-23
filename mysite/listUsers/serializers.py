from rest_framework import serializers

from listUsers.models import ListUser
from lists.serializers import ListSerializer
from users.serializers import UserSerializer

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListUser
        fields = (
            'id',
            'date',
            'list',
            'user'
        )
        