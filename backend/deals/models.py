from django.db import models
from django.conf import settings
from contacts.models import Contact
# Create your models here.
class Deal(models.Model):
    DEAL_STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    name = models.CharField(max_length=255)
    contact = models.ForeignKey(Contact,
        on_delete=models.CASCADE, related_name='deals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,
        choices=DEAL_STATUS_CHOICES, default='new')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='deals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
