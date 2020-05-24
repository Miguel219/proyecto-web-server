from rest_framework import serializers

from messages.models import Message
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    receiver = UserSerializer()
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = (
            'id',
            'content',
            'date',
            'sender',
            'receiver'
        )
        