from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CreditsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "walletapp.credits"
    verbose_name = _("Credits")

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals  # pylint: disable=unused-import
