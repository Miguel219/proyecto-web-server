"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#Configurar urls de aplicacion
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token
)
#Se cargan todos los ViewSets
from users.views import UserViewSet
from comments.views import CommentViewSet
from followers.views import FollowerViewSet
from likes.views import LikeViewSet
from lists.views import ListViewSet
from listUsers.views import ListUserViewSet
from messages.views import MessageViewSet
from chats.views import ChatViewSet
from chatUsers.views import ChatUserViewSet
from retweets.views import RetweetViewSet
from savedTweets.views import SavedTweetViewSet
from tweets.views import TweetViewSet

#Se crea el router que tendra todos los ViewSets
router = routers.DefaultRouter()

#Se agregan todos los ViewSets al router
router.register(r'users', UserViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'followers', FollowerViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'lists', ListViewSet)
router.register(r'listUsers', ListUserViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'chatUsers', ChatUserViewSet)
router.register(r'retweets', RetweetViewSet)
router.register(r'savedTweets', SavedTweetViewSet)
router.register(r'tweets', TweetViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/token-auth/', obtain_jwt_token),
    url(r'^api/v1/token-refresh/', refresh_jwt_token),
]
