import math

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from savedTweets.models import SavedTweet
from savedTweets.serializers import SavedTweetSerializer
from tweets.serializers import TweetSerializer
from retweets.serializers import RetweetSerializer
from users.serializers import UserSerializer


class SavedTweetViewSet(viewsets.ModelViewSet):
    queryset = SavedTweet.objects.all()
    serializer_class = SavedTweetSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='SavedTweetPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': False,
                    'unsave': lambda user, req: user.is_authenticated and req.data['user']==user.id,
                    
                },
                'instance': {
                    'retrieve': lambda user, obj, req: user.is_authenticated,
                    'destroy': 'savedTweets.delete_savedtweet',
                    'update': False,
                }
            }
        ),
    )

    #Cunando se crea la relacion de un tweet guardado por un usuario se asigna el permiso de eliminar
    def perform_create(self, serializer):
        savedTweet = serializer.save()
        user = self.request.user
        assign_perm('savedTweets.delete_savedtweet', user, savedTweet)
        
        return Response(serializer.data)

   #Eliminar un saved tweet
    @action(detail=False, url_path='unsave', methods=['post'])
    def unsave(self, request, pk=None):
        tweet = request.data['tweet']
        user = request.user
        savedTweets = SavedTweet.objects.filter(tweet__exact=tweet,user__exact=user)
        savedTweets.delete()
        return Response(True);