from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL, null=True, blank=True, related_name='received_messages')

    def __str__(self):
        return f"{self.name} - {self.email}"

