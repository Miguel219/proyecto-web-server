import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from followers.models import Follower
from followers.serializers import FollowerSerializer
from users.serializers import UserSerializer


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='FollowerPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    'unfollow': lambda user, req: user.is_authenticated and req.data['userFollower']==user.id,                    
                },
                'instance': {
                    'retrieve': lambda user, obj, req: user.is_authenticated,
                    'destroy': 'followers.delete_follower',
                    'update': False,
                }
            }
        ),
    )

    #Cunando se crea el seguidor asignar permiso de eliminar
    def perform_create(self, serializer):
        follower = serializer.save()
        user = self.request.user
        assign_perm('followers.delete_follower', user, follower)
        
        return Response(serializer.data)

    #Eliminar un Follow
    @action(detail=False, url_path='unfollow', methods=['post'])
    def unfollow(self, request, pk=None):
        userFollower = request.data['userFollower']
        userFollowing = request.data['userFollowing']
        follower = Follower.objects.filter(userFollower__exact=userFollower,userFollowing__exact=userFollowing)
        follower.delete()
        return Response(True);     