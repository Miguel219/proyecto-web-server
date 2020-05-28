import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from chats.models import Chat
from chats.serializers import ChatSerializer
from chatUsers.models import ChatUser
from messages.models import Message
from messages.serializers import MessageSerializer

def check_chatUser(user, obj, request):
    chatUser = ChatUser.objects.filter(chat=obj, user=user)
    return user.is_authenticated and chatUser.count() == 1

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='ChatPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    
                },
                'instance': {
                    'retrieve': False,
                    'destroy': 'chats.delete_chat',
                    'update': False,
                    'get_chatMessages': check_chatUser,
                }
            }
        ),
    )

    #Cunando se crea el chat asignar permiso de eliminar
    def perform_create(self, serializer):
        chat = serializer.save()
        user = self.request.user
        assign_perm('chats.delete_chat', user, chat)
        
        return Response(serializer.data)
        
    #Obtener los mensajes de un chat
    @action(detail=True, url_path='chatMessages', methods=['get'])
    def get_chatMessages(self, request, pk=None):
        
        chat = self.get_object()
        chatMessages = Message.objects.filter(chat=chat.id).order_by('date')
        if(chatMessages.count()>0):
            return(Response(MessageSerializer(chatMessages,many=True,context={'request':request}).data))
        else:
            return Response([])