# backend/apps/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # <- important for custom user reference

class User(AbstractUser):
    """
    Custom user model extending AbstractUser.
    - role: controls permissions across the CRM.
    """
    ROLE_ADMIN = "admin"
    ROLE_MANAGER = "manager"
    ROLE_SALES = "sales"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_MANAGER, "Manager"),
        (ROLE_SALES, "Sales"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_SALES)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Profile(models.Model):
    """
    Simple Profile for additional user info.
    Linked OneToOne to User.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # safer for custom User
        on_delete=models.CASCADE,
        related_name="profile",
        null=True,   # allow null for existing rows
        blank=True   # optional for forms/admin
    )
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.user.username if self.user else 'No User'}"
