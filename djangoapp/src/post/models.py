import datetime

from django.db import models
from django.utils import timezone
from appUser.models import appUser

# Create your models here.
class post(models.Model):
    Post_id         =   models.AutoField(primary_key=True)
    Username        =   models.ForeignKey(appUser, on_delete=models.CASCADE)
    Pub_date        =   models.DateTimeField('data posted')
    Apartment       =   models.CharField(max_length=60)
    Post_title      =   models.TextField()
    # Description     =   models.TextField()
    # Move_in_date    =   models.DateField()
    # Move_out_date   =   models.DateField()
    # Duration        =   models.IntegerField()
    
    def __str__(self):
        return self.Username

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
