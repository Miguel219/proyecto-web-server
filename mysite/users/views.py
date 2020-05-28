import math
from itertools import chain
from django.db.models import Max, F

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from users.models import User
from users.serializers import UserSerializer
from tweets.models import Tweet 
from tweets.serializers import TweetSerializer 
from retweets.models import Retweet 
from retweets.serializers import RetweetSerializer 
from likes.models import Like 
from likes.serializers import LikeSerializer 
from followers.models import Follower
from followers.serializers import FollowerSerializer
from messages.models import Message
from messages.serializers import MessageSerializer
from chatUsers.models import ChatUser 
from chatUsers.serializers import ChatUserSerializer
from chats.models import Chat 
from chats.serializers import ChatSerializer
from lists.models import List
from lists.serializers import ListSerializer
from savedTweets.models import SavedTweet
from savedTweets.serializers import SavedTweetSerializer

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
                    'get_tweets': lambda user, obj, req: user.is_authenticated,
                    'get_likedTweets': lambda user, obj, req: user.is_authenticated,
                    'get_followingTweets': lambda user, obj, req: user.is_authenticated,
                    'get_followers': lambda user, obj, req: user.is_authenticated,
                    'get_following': lambda user, obj, req: user.is_authenticated,
                    'get_usersSearch': lambda user, obj, req: user.is_authenticated,
                    'get_tweetsSearch': lambda user, obj, req: user.is_authenticated,
                    'get_messages': lambda user, obj, req: user.is_authenticated,
                    'get_lists': lambda user, obj, req: user.is_authenticated,
                    'get_savedTweets': lambda user, obj, req: user.is_authenticated,

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

    #Obtener los tweets y retweets de un usuario
    @action(detail=True, url_path='tweets', methods=['get'])
    def get_tweets(self, request, pk=None):
        
        user = self.get_object()
        tweets = Tweet.objects.filter(user=user.id)
        retweets = Retweet.objects.filter(user=user.id)
        #Se unen los querySets
        results_list = list(chain(tweets, retweets))
        #Se filtran por fechas
        sorted_list = sorted(results_list, key=lambda instance: instance.date, reverse=True)
        # Build the list with items based on the FeedItemSerializer fields
        results = list()
        for entry in sorted_list:
            item_type = entry.__class__.__name__.lower()
            if isinstance(entry, Tweet):
                serializer = TweetSerializer(entry,context={'request':request})
            if isinstance(entry, Retweet):
                serializer = RetweetSerializer(entry,context={'request':request})

            results.append({'id': item_type + '-' + str(serializer.data['id']), 'itemType': item_type, 'data': serializer.data})

        return(Response(results))

    #Obtener los tweets y retweets que le han gustado a un usuario
    @action(detail=True, url_path='likedTweets', methods=['get'])
    def get_likedTweets(self, request, pk=None):
        
        user = self.get_object()
        tweets = Tweet.objects.filter(id__in=Like.objects.filter(user=user.id).values('tweet'))
        retweets = Retweet.objects.filter(id__in=Like.objects.filter(user=user.id).values('retweet'))
        #Se unen los querySets
        results_list = list(chain(tweets, retweets))
        #Se filtran por fechas
        sorted_list = sorted(results_list, key=lambda instance: instance.date, reverse=True)
        # Build the list with items based on the FeedItemSerializer fields
        results = list()
        for entry in sorted_list:
            item_type = entry.__class__.__name__.lower()
            if isinstance(entry, Tweet):
                serializer = TweetSerializer(entry,context={'request':request})
            if isinstance(entry, Retweet):
                serializer = RetweetSerializer(entry,context={'request':request})

            results.append({'id': item_type + '-' + str(serializer.data['id']), 'itemType': item_type, 'data': serializer.data})

        return(Response(results))
    
    #Obtener los tweets y retweets de los usuarios que sigue un usuario
    @action(detail=True, url_path='followingTweets', methods=['get'])
    def get_followingTweets(self, request, pk=None):
        
        user = self.get_object()
        #Se guardan los ids de los usuarios que sigue el usuario
        following = Follower.objects.filter(userFollower=user.id)
        usersFollowing = [ userF.userFollowing.id for userF in following ]
        #Se agrega el id del usuario
        usersFollowing.append(user.id)
        #Se consultan los tweets y retweets de todos los usuarios en la lista 
        tweets = Tweet.objects.filter(user__in=usersFollowing)
        retweets = Retweet.objects.filter(user__in=usersFollowing)
        #Se unen los querySets
        results_list = list(chain(tweets, retweets))
        #Se filtran por fechas
        sorted_list = sorted(results_list, key=lambda instance: instance.date, reverse=True)
        # Build the list with items based on the FeedItemSerializer fields
        results = list()
        for entry in sorted_list:
            item_type = entry.__class__.__name__.lower()
            if isinstance(entry, Tweet):
                serializer = TweetSerializer(entry,context={'request':request})
            if isinstance(entry, Retweet):
                serializer = RetweetSerializer(entry,context={'request':request})

            results.append({'id': item_type + '-' + str(serializer.data['id']), 'itemType': item_type, 'data': serializer.data})

        return(Response(results))
        
    #Obtener los followers de un usuario
    @action(detail=True, url_path='followers', methods=['get'])
    def get_followers(self, request, pk=None):
        
        user = self.get_object()
        followers = User.objects.filter(id__in=Follower.objects.filter(userFollowing=user.id).order_by('date').values('userFollower'))
        if(followers.count()>0):
            return(Response(UserSerializer(followers,many=True,context={'request':request}).data))
        else:
            return Response([])
        
    #Obtener los following de un usuario
    @action(detail=True, url_path='following', methods=['get'])
    def get_following(self, request, pk=None):
        
        user = self.get_object()
        following  = User.objects.filter(id__in=Follower.objects.filter(userFollower=user.id).order_by('date').values('userFollowing'))
        if(following.count()>0):
            return(Response(UserSerializer(following,many=True,context={'request':request}).data))
        else:
            return Response([])
        
    #Obtener los usuarios del search
    @action(detail=False, url_path='usersSearch', methods=['post'])
    def get_usersSearch(self, request, pk=None):
        
        user = request.user
        search = request.data['search']
        users = User.objects.exclude(username=user).filter(username__icontains=search)
        if(users.count()>0):
            return(Response(UserSerializer(users,many=True,context={'request':request}).data))
        else:
            return Response([])
        
    #Obtener los tweets del search
    @action(detail=False, url_path='tweetsSearch', methods=['post'])
    def get_tweetsSearch(self, request, pk=None):
        search = request.data['search']
        tweets = Tweet.objects.filter(content__icontains=search)
        retweets = Retweet.objects.filter(content__icontains=search)
        #Se unen los querySets
        results_list = list(chain(tweets, retweets))
        #Se filtran por fechas
        sorted_list = sorted(results_list, key=lambda instance: instance.date, reverse=True)
        # Build the list with items based on the FeedItemSerializer fields
        results = list()
        for entry in sorted_list:
            item_type = entry.__class__.__name__.lower()
            if isinstance(entry, Tweet):
                serializer = TweetSerializer(entry,context={'request':request})
            if isinstance(entry, Retweet):
                serializer = RetweetSerializer(entry,context={'request':request})

            results.append({'id': item_type + '-' + str(serializer.data['id']), 'itemType': item_type, 'data': serializer.data})

        return(Response(results))
        
    #Obtener los messages de un usuario
    @action(detail=True, url_path='messages', methods=['get'])
    def get_messages(self, request, pk=None):
        
        user = self.get_object()
        messages = Message.objects.filter(chat__in=ChatUser.objects.filter(user=user).values('chat'))
        lastMessages = list(messages.values('chat','content','date').filter(
            date__in=messages.values('chat').annotate(lastdate=Max('date')).values('lastdate'),
            chat__in=messages.values('chat').annotate(lastdate=Max('date')).values('chat')).order_by('chat'))
        chatUser = list(ChatUser.objects.exclude(user=user).filter(chat__in=messages.values('chat')).annotate(username=F('user__username'),userid=F('user__id'),first_name=F('user__first_name')).values('chat','userid','username','first_name').order_by('chat'))
        userMessages = []
        for i in range(len(lastMessages)):
            if lastMessages[i]['chat'] == chatUser[i]['chat']:
                userMessages.append({**lastMessages[i], **chatUser[i]})
        #Se filtran por fechas
        sorted_userMessages = sorted(userMessages, key=lambda instance: instance['date'], reverse=True)
        return(Response(sorted_userMessages))
        
    #Obtener las listas de un usuario
    @action(detail=True, url_path='lists', methods=['get'])
    def get_lists(self, request, pk=None):
        
        user = self.get_object()
        lists = List.objects.filter(owner=user.id).order_by('date')
        if(lists.count()>0):
            return(Response(ListSerializer(lists,many=True).data))
        else:
            return Response([])
        


    #Obtener los tweets guardados por el usuario de un usuario
    @action(detail=True, url_path='savedTweets', methods=['get'])
    def get_savedTweets(self, request, pk=None):
        user = self.get_object()
        #Se consultan los tweets y retweets de todos los usuarios en la lista 
        tweets = Tweet.objects.filter(id__in=SavedTweet.objects.filter(user=user.id).order_by('date').values('tweet'))
        retweets = Retweet.objects.filter(id__in=SavedTweet.objects.filter(user=user.id).order_by('date').values('retweet'))
        #Se unen los querySets
        results_list = list(chain(tweets, retweets))
        #Se filtran por fechas
        sorted_list = sorted(results_list, key=lambda instance: instance.date, reverse=True)
        # Build the list with items based on the FeedItemSerializer fields
        results = list()
        for entry in sorted_list:
            item_type = entry.__class__.__name__.lower()
            if isinstance(entry, Tweet):
                serializer = TweetSerializer(entry,context={'request':request})
            if isinstance(entry, Retweet):
                serializer = RetweetSerializer(entry,context={'request':request})

            results.append({'id': item_type + '-' + str(serializer.data['id']), 'itemType': item_type, 'data': serializer.data})

        return(Response(results))