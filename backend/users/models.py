from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Customer User Model inherting from Abstarctuser Because it gives us flexibility to add 
# custome fields(phone, company, etc)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('sales', 'Sales'),
    )
    role = models.CharField(max_length=20,
        choices=ROLE_CHOICES,
        default='Sales')
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    

class Profile(models.Model):
    user = models.OneToOneField(User,
        on_delete=models.CASCADE, related_name='profile'),
    bio = models.TextField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"profile of {self.user.username}"