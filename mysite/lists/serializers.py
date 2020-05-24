from rest_framework import serializers

from lists.models import List
from users.serializers import UserSerializer

class ListSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = List
        fields = (
            'id',
            'name',
            'date',
            'owner'
        )
        