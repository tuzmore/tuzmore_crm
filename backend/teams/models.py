from django.db import models
from users.models import User
from contacts.models import Contact
from django.utils import timezone
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Assignment(models.Model):
    ASSIGN_TYPE = (
        ('CONTACT', 'Contact'),
        ('DEAL', 'Deal'),
        ('TASK', 'Task'),
    )

    assign_type = models.CharField(max_length=20, choices=ASSIGN_TYPE)
    contact = models.ForeignKey(Contact,
        on_delete =models.CASCADE, blank=True, null=True)
    assigned_to_user = models.ForeignKey(User, 
        on_delete =models.CASCADE, blank=True, null=True, related_name='assignments')
    assigned_to_team = models.ForeignKey(Team,
        on_delete =models.CASCADE, blank=True, null=True, related_name='assignments')
    created_by = models.ForeignKey(User,
        on_delete =models.CASCADE, related_name='created_assignments')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.assign_type} assigned by {self.created_by.username}"