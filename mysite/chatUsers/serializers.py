from rest_framework import serializers

from chatUsers.models import ChatUser
from users.serializers import UserSerializer
from chats.serializers import ChatSerializer
from users.models import User
from chats.models import Chat

class ChatUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatUser
        fields = (
            'id',
            'chat',
            'user'
        )

    #Funcion de representacion que realiza un override al serializer
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        data['user'] = UserSerializer(
            User.objects.get(pk=data['user']),context={'request':request}).data
        data['chat'] = ChatSerializer(
            Chat.objects.get(pk=data['chat']),context={'request':request}).data
        return data
        