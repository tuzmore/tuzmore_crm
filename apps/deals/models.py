from django.db import models
from django.conf import settings

from apps.contacts.models import Contact
from apps.companies.models import Company

# Create your models here.

class Deal(models.Model):

    STAGES = [
        ("lead", "Lead"),
        ("qualified", "Qualified"),
        ("proposal", "Proposal"),
        ("negotiation", "Negotiation"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255
    )

    value = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    stage = models.CharField(
        max_length=20,
        choices=STAGES,
        default="lead"
    )

    expected_close_date = models.DateField()

    note = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
