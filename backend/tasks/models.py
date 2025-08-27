from django.db import models
from django.conf import settings
from contacts.models import Contact
from deals.models import Deal
# Create your models here.

User= settings.AUTH_USER_MODEL
# Task model: work assigned to a user(e.g follow-up call)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    assigned_to = models.ForeignKey(User,
        on_delete=models.CASCADE, related_name='tasks')
    contact = models.ForeignKey(Contact,
        on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    deal = models.ForeignKey(Deal, 
        on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.assigned_to}"
    

# Activity model:Logs of actions(calls, meetings, notes)
class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('email', 'Email'),
    )

    type = models.CharField(max_length=20,
        choices=ACTIVITY_TYPES)
    description = models.TextField()

    user = models.ForeignKey(User,
        on_delete=models.CASCADE, related_name='activities')
    contact = models.ForeignKey(Contact,
        on_delete=models.CASCADE, blank=True, null=True, related_name='activities')
    deal = models.ForeignKey(Deal,
        on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.user}"