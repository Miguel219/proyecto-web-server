import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from users.serializers import UserSerializer
from users.models import User
from retweets.models import Retweet
from comments.models import Comment
from comments.serializers import CommentSerializer
from likes.models import Like
from likes.serializers import LikeSerializer


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
                    'get_likes': lambda user, obj, req: user.is_authenticated,
                    'get_users_likes_tweet': lambda user, obj, req: user.is_authenticated,
                    'get_users_retweets_tweet': lambda user, obj, req: user.is_authenticated,
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
        comments = Comment.objects.filter(tweet=tweet.id).order_by('date')
        if(comments.count()>0):
            return(Response(CommentSerializer(comments,many=True,context={'request':request}).data))
        else:
            return Response([])

    #Obtener los likes de un tweet
    @action(detail=True, url_path='likes', methods=['get'])
    def get_likes(self, request, pk=None):
        
        tweet = self.get_object()
        likes = Like.objects.filter(tweet=tweet.id).order_by('date')
         
        if(likes.count()>0):
            return(Response(LikeSerializer(likes,many=True,context={'request':request}).data))
        else:
            return Response([])
    
    #Obtener los usuarios que le dieron like a un tweet
    @action(detail=True, url_path='likesUsers', methods=['get'])
    def get_users_likes_tweet(self, request, pk=None):
        
        tweet = self.get_object()
        likes = Like.objects.filter(tweet=tweet.id).order_by('date').values('user')
        users = User.objects.filter(id__in=likes)
        if(users.count()>0):
            return(Response(UserSerializer(users,many=True,context={'request':request}).data))
        else:
            return Response([])

    #Obtener los usuarios que le dieron retweet a un tweet
    @action(detail=True, url_path='retweetUsers', methods=['get'])
    def get_users_retweets_tweet(self, request, pk=None):
        
        tweet = self.get_object()
        retweets = Retweet.objects.filter(originalTweet=tweet.id).order_by('date').values('user')
        users = User.objects.filter(id__in=retweets)
        if(users.count()>0):
            return(Response(UserSerializer(users,many=True,context={'request':request}).data))
        else:
            return Response([])