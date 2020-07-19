from django.db import models

# Create your models here.
class appUser(models.Model):
    Name     =   models.CharField(max_length=36)
    Email    =   models.EmailField(max_length=100)
    Username =   models.CharField(max_length=36)
    Password =   models.CharField(max_length=32)