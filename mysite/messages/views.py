import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from messages.models import Message
from messages.serializers import MessageSerializer
from users.serializers import UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='MessagePermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
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
        