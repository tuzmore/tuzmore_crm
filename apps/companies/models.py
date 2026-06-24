from django.db import models
from django.conf import settings

# Create your models here.

class Company(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=255
    )

    email = models.CharField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    industry = models.CharField(
        max_length=100,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return self.name