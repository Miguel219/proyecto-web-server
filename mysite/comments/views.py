import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from comments.models import Comment
from comments.serializers import CommentSerializer
from users.serializers import UserSerializer
from tweets.serializers import TweetSerializer
from retweets.serializers import RetweetSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='CommentPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    
                },
                'instance': {
                    'retrieve': lambda user, obj, req: user.is_authenticated,
                    'destroy': 'comments.delete_comment',
                    'update': False,
                }
            }
        ),
    )

    #Cunando se crea el comment asignar permiso de eliminar
    def perform_create(self, serializer):
        comment = serializer.save()
        user = self.request.user
        assign_perm('comments.delete_comment', user, comment)
        
        return Response(serializer.data)