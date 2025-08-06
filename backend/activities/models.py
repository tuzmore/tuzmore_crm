from django.db import models
from django.contrib.auth import get_user_model
from deals.models import Deal
# Create your models here.

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.CharField(max_length=20,
        choices=ACTIVITY_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type.title()} - {self.timestamp.date()}"

