from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import appuser

# Althogh we used RAW SQL to insert into appUser
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        appUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.appUser.save()