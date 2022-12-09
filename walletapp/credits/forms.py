from django import forms

from .choices import CREDIT_ACTIVE, CREDIT_STATUS_CHOICES
from .models import Credit


class CreditForm(forms.ModelForm):
    concept = forms.CharField(label="")
    amount = forms.IntegerField(label="")
    status = forms.ChoiceField(
        label=None,
        choices=CREDIT_STATUS_CHOICES,
        initial=CREDIT_ACTIVE,
        required=False,
        widget=forms.Select(
            attrs={
                "disabled": "true",
                "class": "form-control br-8px",
            },
        ),
    )

    class Meta:
        model = Credit
        fields = [
            "concept",
            "amount",
            "status",
        ]
