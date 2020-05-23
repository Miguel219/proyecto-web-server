from django.db import models
from django.contrib.auth.models import User as UserDjango


#Clase User que tiene una relacion uno a uno con un usuario de Django
class User(models.Model):
    name = models.CharField(max_length=200)
    userDjango = models.OneToOneField(UserDjango, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name