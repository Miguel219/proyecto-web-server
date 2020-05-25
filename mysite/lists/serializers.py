from rest_framework import serializers

from lists.models import List
from users.models import User
from users.serializers import UserSerializer

class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = (
            'id',
            'name',
            'date',
            'owner'
        )
        
    #Funcion de representacion que realiza un override al serializer
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['owner'] = UserSerializer(
            User.objects.get(pk=data['owner'])).data
        return data