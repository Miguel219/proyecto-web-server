import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from lists.models import List
from lists.serializers import ListSerializer
from users.serializers import UserSerializer


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='ListPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    
                },
                'instance': {
                    'retrieve': 'lists.view_list',
                    'destroy': 'lists.delete_list',
                    'update': 'lists.change_list',
                }
            }
        ),
    )

    #Cunando se crea la lista asignar permiso de eliminar, ver y editar
    def perform_create(self, serializer):
        selfList = serializer.save()
        user = self.request.user
        assign_perm('lists.view_list', user, selfList)
        assign_perm('lists.delete_list', user, selfList)
        assign_perm('lists.change_list', user, selfList)
        
        return Response(serializer.data)
        