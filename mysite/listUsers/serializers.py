from rest_framework import serializers

from listUsers.models import ListUser
from lists.models import List
from lists.serializers import ListSerializer
from users.models import User
from users.serializers import UserSerializer

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListUser
        fields = (
            'id',
            'date',
            'list',
            'user'
        )
        
    #Funcion de representacion que realiza un override al serializer
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        data['list'] = ListSerializer(
            List.objects.get(pk=data['list']),context={'request':request}).data
        data['user'] = UserSerializer(
            User.objects.get(pk=data['user']),context={'request':request}).data
        return data