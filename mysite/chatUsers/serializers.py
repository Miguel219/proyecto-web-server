from rest_framework import serializers

from chatUsers.models import ChatUser
from users.serializers import UserSerializer
from chats.serializers import ChatSerializer

class ChatUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatUser
        fields = (
            'id',
            'chat',
            'user'
        )
        