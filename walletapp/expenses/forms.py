from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):
    concept = forms.CharField(label="")
    amount = forms.IntegerField(label="")

    class Meta:
        model = Expense
        fields = [
            "concept",
            "amount",
        ]
