from django.db import models
from django.db import connection

# Create your models here.
class appUser(models.Model):
    Name     =   models.CharField(max_length=36)
    Email    =   models.EmailField(max_length=100, unique=True)
    Username =   models.CharField(max_length=36, primary_key=True)
    Password =   models.CharField(max_length=32)
    phone    =   models.CharField(max_length=11, unique=True)
