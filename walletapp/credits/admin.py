from django.contrib import admin

from walletapp.credits.models import Credit


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = (
        "concept",
        "amount",
        "status",
    )

    search_fields = (
        "concept",
        "amount",
        "status",
    )
