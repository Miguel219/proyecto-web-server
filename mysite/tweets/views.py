import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from users.serializers import UserSerializer
from comments.models import Comment
from comments.serializers import CommentSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='TweetPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    
                },
                'instance': {
                    'retrieve': lambda user, obj, req: user.is_authenticated,
                    'destroy': 'tweets.delete_tweet',
                    'update': False,
                    'get_comments': lambda user, obj, req: user.is_authenticated,
                }
            }
        ),
    )

    #Cunando se crea el tweet asignar permiso de eliminar
    def perform_create(self, serializer):
        tweet = serializer.save()
        user = self.request.user
        assign_perm('tweets.delete_tweet', user, tweet)
        
        return Response(serializer.data)

    #Obtener los comentarios de un tweet
    @action(detail=True, url_path='comments', methods=['get'])
    def get_comments(self, request, pk=None):
        
        tweet = self.get_object()
        comments = Comment.objects.filter(tweet=tweet.id)
        if(comments.count()>0):
            return(Response(CommentSerializer(comments,many=True).data))
        else:
            return Response([])