from django.db import models

# Create your models here.
class apartment(models.Model):
    ApartmentID     =   models.AutoField(primary_key=True)
    Name            =   models.CharField(max_length=60, unique=True)
    Description_a   =   models.TextField(blank=True)
    Location        =   models.TextField(blank=True)
    Email           =   models.CharField(max_length=30)
    Phone           =   models.CharField(max_length=11)
    Pet_friendly    =   models.BooleanField()
    Printer         =   models.BooleanField()
    Swimming_pool   =   models.BooleanField()
    Gym             =   models.BooleanField()