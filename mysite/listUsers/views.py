import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from listUsers.models import ListUser
from listUsers.serializers import ListUserSerializer
from lists.serializers import ListSerializer
from users.serializers import UserSerializer


class ListUserViewSet(viewsets.ModelViewSet):
    queryset = ListUser.objects.all()
    serializer_class = ListUserSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='ListUserPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    
                },
                'instance': {
                    'retrieve': False,
                    'destroy': 'listUsers.delete_listuser',
                    'update': False,
                }
            }
        ),
    )

    #Cunando se crea la relacion de la lista con el usuario se asigna el permiso de eliminar
    def perform_create(self, serializer):
        listUser = serializer.save()
        user = self.request.user
        assign_perm('listUsers.delete_listuser', user, listUser)
        
        return Response(serializer.data)
        