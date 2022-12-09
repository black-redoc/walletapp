from django.db.models.signals import post_save
from django.dispatch import receiver

from .choices import CREDIT_PAID
from .models import Credit


@receiver(post_save, sender=Credit)
def set_credit_as_paid_when_amount_is_zero(
    sender, instance: Credit, created: bool, **kwargs
) -> None:
    if created:
        # this executes when credit instance is created and not updated
        return
    if instance.amount == 0:
        Credit.objects.filter(pk=instance.pk).update(status=CREDIT_PAID)
