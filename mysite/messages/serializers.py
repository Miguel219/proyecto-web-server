from rest_framework import serializers

from messages.models import Message
from users.models import User
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'id',
            'content',
            'date',
            'sender',
            'chat'
        )
        
    #Funcion de representacion que realiza un override al serializer
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        data['sender'] = UserSerializer(
            User.objects.get(pk=data['sender']),context={'request':request}).data
        return data