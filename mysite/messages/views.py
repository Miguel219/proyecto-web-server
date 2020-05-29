import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from messages.models import Message
from messages.serializers import MessageSerializer
from users.serializers import UserSerializer
from chats.serializers import ChatSerializer
from chatUsers.serializers import ChatUserSerializer
from chatUsers.models import ChatUser

def check_chatUser(user,request):
    chatId = request.data['chat']
    chatUser = ChatUser.objects.filter(chat=chatId, user=user)
    return user.is_authenticated and chatUser.count() == 1

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='MessagePermission',
            permission_configuration={
                'base': {
                    'create': check_chatUser,
                    'list': False,
                    
                },
                'instance': {
                    'retrieve': False,
                    'destroy': 'messages.delete_message',
                    'update': False,
                }
            }
        ),
    )

    #Cunando se crea el mensaje asignar permiso de eliminar
    def perform_create(self, serializer):
        message = serializer.save()
        user = self.request.user
        assign_perm('messages.delete_message', user, message)
        
        return Response(serializer.data)
        