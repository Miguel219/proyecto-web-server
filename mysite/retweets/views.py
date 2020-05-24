import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from retweets.models import Retweet
from retweets.serializers import RetweetSerializer
from users.serializers import UserSerializer
from tweets.serializers import TweetSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer
from likes.models import Like
from likes.serializers import LikeSerializer


class RetweetViewSet(viewsets.ModelViewSet):
    queryset = Retweet.objects.all()
    serializer_class = RetweetSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='RetweetPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    
                },
                'instance': {
                    'retrieve': lambda user, obj, req: user.is_authenticated,
                    'destroy': 'retweets.delete_retweet',
                    'update': False,
                    'get_comments': lambda user, obj, req: user.is_authenticated,
                    'get_likes': lambda user, obj, req: user.is_authenticated,
                }
            }
        ),
    )

    #Cunando se crea el retweet asignar permiso de eliminar
    def perform_create(self, serializer):
        retweet = serializer.save()
        user = self.request.user
        assign_perm('retweets.delete_retweet', user, retweet)
        
        return Response(serializer.data)

    #Obtener los comentarios de un retweet
    @action(detail=True, url_path='comments', methods=['get'])
    def get_comments(self, request, pk=None):
        
        retweet = self.get_object()
        comments = Comment.objects.filter(retweet=retweet.id).order_by('date')
        if(comments.count()>0):
            return(Response(CommentSerializer(comments,many=True).data))
        else:
            return Response([])

    #Obtener los likes de un retweet
    @action(detail=True, url_path='likes', methods=['get'])
    def get_likes(self, request, pk=None):
        
        retweet = self.get_object()
        likes = Like.objects.filter(retweet=retweet.id).order_by('date')
        if(likes.count()>0):
            return(Response(LikeSerializer(likes,many=True).data))
        else:
            return Response([])