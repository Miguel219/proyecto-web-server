import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from chatUsers.models import ChatUser
from chatUsers.serializers import ChatUserSerializer
from users.serializers import UserSerializer
from chats.serializers import ChatSerializer


class ChatUserViewSet(viewsets.ModelViewSet):
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='ChatUserPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    
                },
                'instance': {
                    'retrieve': False,
                    'destroy': 'ChatUsers.delete_chatuser',
                    'update': False,
                }
            }
        ),
    )

    #Cuando se crea la relacion del chat con el usuario asignar permiso de eliminar esa relacion
    def perform_create(self, serializer):
        chatUser = serializer.save()
        user = self.request.user
        assign_perm('ChatUsers.delete_chatuser', user, chatUser)
        
        return Response(serializer.data)
        