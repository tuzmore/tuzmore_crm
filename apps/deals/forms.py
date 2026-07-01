from django import forms
from .models import Deal

class DealForm(forms.ModelForm):

    class Meta:
        model = Deal
        
        fields = [
            "contact",
            "company",
            "title",
            "value",
            "stage",
            "expected_close_date",
            "notes",
        ]