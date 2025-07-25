from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Keep username field but make email unique and required
    email = models.EmailField(_('email address'), unique=True)
    
    # Add CRM-specific fields
    company = models.CharField(max_length=100, blank=True)
    subscription_plan = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('pro', 'Professional'),
            ('enterprise', 'Enterprise')
        ],
        default='free'
    )
    
    # Set email as authentication identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required for createsuperuser
    
    def __str__(self):
        return self.email