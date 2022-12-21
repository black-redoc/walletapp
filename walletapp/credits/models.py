from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import CREDIT_ACTIVE, CREDIT_STATUS_CHOICES


class Credit(models.Model):
    concept = models.CharField(_("Concept"), max_length=80)
    amount = models.BigIntegerField(_("Amount"))
    status = models.CharField(
        _("status"),
        choices=CREDIT_STATUS_CHOICES,
        default=CREDIT_ACTIVE,
        max_length=len(CREDIT_ACTIVE),
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def add_payment(self, amount_payment: int):
        if not amount_payment <= self.amount:
            raise ValueError("The amount is less thant the payment value.")
        self.amount -= amount_payment

    @property
    def get_created_at(self) -> str:
        return self.created_at.strftime("%Y-%m-%d")

    @property
    def get_full_created_at(self) -> str:
        return self.created_at.strftime("%d/%m/%Y")

    @property
    def get_full_updated_at(self) -> str:
        return self.updated_at.strftime("%d/%m/%Y")

    def __str__(self):
        return (
            f'{{"pk": {self.pk}, "concept": "{self.concept}",'
            + f'"created_at": "{self.get_full_created_at}",'
            + f'"status": "{self.status}"}}'
        )
