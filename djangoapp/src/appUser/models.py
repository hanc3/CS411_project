from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class appUser(models.Model):
    user        =   models.OneToOneField(User, on_delete=models.CASCADE)
    username    =   models.CharField(max_length=255,blank=True)
    image       =   models.ImageField(default='default.jpg', upload_to='profile_pics')
    gender      =   models.CharField(max_length=10,blank=True)
    bio         =   models.CharField(max_length=500,blank=True)
    phone       =   models.CharField(max_length=15,blank=True)
    num_of_post =   models.IntegerField(default=0)

    def __str__(self):
        return "ID:{:<5}".format(self.user.id) + "USERNAME: {}".format(self.user.username) 
