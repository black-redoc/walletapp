from django.forms import CharField, IntegerField, ModelForm

from .models import Income


class IncomeForm(ModelForm):
    concept = CharField(label="")
    amount = IntegerField(label="")

    class Meta:
        model = Income
        fields = ["concept", "amount"]
