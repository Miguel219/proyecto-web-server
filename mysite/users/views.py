from django.shortcuts import render
import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from users.models import User
from users.serializers import UserSerializer

# Clase UserViewSet

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='UsersPermissions',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                    
                },
                'instance': {
                    'retrieve': True,
                    'destroy': 'users.delete_user',
                    'update': 'users.change_user',
                    'partial_update': 'users.change_user',
                    'set_password': 'users.change_user',

                }
            }
        ),
    )
    
    #Dar permisos al usuario sobre el mismo
    def perform_create(self, serializer):
        user = serializer.save()
        print(user.password)
        user.set_password(user.password)
        user.save()
        assign_perm('users.delete_user', user, user)
        assign_perm('users.change_user', user, user)
        
        return Response(serializer.data)

    #Cambiar contraseña
    @action(detail=True, url_path='password', methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        queryData=request.data
        data = dict(queryData)
        password = (data['password'][0])
        user.set_password(password)
        user.save()
        return(Response(UserSerializer(user).data))
 
        
