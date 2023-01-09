from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .utils import create_avatar


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, profile_image=create_avatar(instance.email))

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()