from rest_framework import serializers

from parents.models import User

#Clase User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'userDjango_id',
            'userDjango'
            'name',
        )