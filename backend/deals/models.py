from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Deal(models.Model):
    STAGE_CHOICES = [
        ('prospect','Prospect'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal sent'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    title = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=20,
        choices=STAGE_CHOICES, default='prospect')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.stage}"