from django.db import models
from django.contrib.auth.models import User as UserDjango


#Clase User que tiene una relacion uno a uno con un usuario de Django
class User(UserDjango):
    
    def __str__(self):
        return self.first_name +" " +self.last_name