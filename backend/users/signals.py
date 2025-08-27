from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(users=instance)

def save_profile(sender, instance, **kwargs):
    instance.profile.save()