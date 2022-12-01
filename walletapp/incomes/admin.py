from django.contrib import admin

from walletapp.incomes.models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        "concept",
        "amount",
    )
