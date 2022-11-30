from django.contrib import admin

from walletapp.expenses.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "concept",
        "amount",
    )
