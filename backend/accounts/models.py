from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/profile/ {filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return self.user.username
