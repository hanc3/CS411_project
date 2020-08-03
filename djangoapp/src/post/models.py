import datetime

from django.db import models
from django.utils import timezone
from appUser.models import appUser
from apartment.models import apartment

# Create your models here.
class post(models.Model):
    Post_id         =   models.AutoField(primary_key=True)
    id              =   models.ForeignKey(appUser, on_delete=models.CASCADE)
    Pub_date        =   models.DateTimeField('data posted')
    ApartmentID     =   models.ForeignKey(apartment, on_delete=models.CASCADE)
    Apartment       =   models.CharField(max_length=60)
    Post_title      =   models.TextField()
    Description     =   models.TextField(blank=True)
    Move_in_date    =   models.DateField()
    Move_out_date   =   models.DateField()
    Duration        =   models.IntegerField()
    Price           =   models.DecimalField(max_digits=7, decimal_places=2)
    Exist           =   models.BooleanField(default=True)
    Bedroom         =   models.IntegerField()
    Bathroom        =   models.IntegerField()
    Likes           =   models.IntegerField()
    Views           =   models.IntegerField()

class view_history(models.Model):
    id          =   models.ForeignKey(appUser, on_delete=models.CASCADE)
    Post_id     =   models.ForeignKey(post, on_delete=models.CASCADE)
    View_time   =   models.DateTimeField(primary_key=True)

class search_history(models.Model):
    id              =   models.ForeignKey(appUser, on_delete=models.CASCADE)
    Search_time     =   models.DateTimeField(primary_key=True)
    Move_in_date    =   models.DateField()
    Move_out_date   =   models.DateField()
    Duration        =   models.IntegerField()
    Price           =   models.DecimalField(max_digits=7, decimal_places=2)
    Bedroom         =   models.IntegerField()
    Bathroom        =   models.IntegerField()
    Pet_friendly    =   models.IntegerField()
    Printer         =   models.IntegerField()
    Swimming_pool   =   models.IntegerField()
    Gym             =   models.IntegerField()

