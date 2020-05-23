import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from likes.models import Like
from likes.serializers import LikeSerializer
from users.serializers import UserSerializer
from tweets.serializers import TweetSerializer
from retweets.serializers import RetweetSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='LikePermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    
                },
                'instance': {
                    'retrieve': lambda user, obj, req: user.is_authenticated,
                    'destroy': 'likes.delete_like',
                    'update': False,
                }
            }
        ),
    )

    #Cunando se crea el like asignar permiso de eliminar
    def perform_create(self, serializer):
        like = serializer.save()
        user = self.request.user
        assign_perm('likes.delete_like', user, like)
        
        return Response(serializer.data)