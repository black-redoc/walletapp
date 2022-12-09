from django.shortcuts import render
from django.views.generic import View

from walletapp.credits.models import Credit
from walletapp.expenses.models import Expense
from walletapp.incomes.models import Income

from .repository import (
    get_flatten_lists,
    get_model_with_kind_property,
    get_total_amount,
)


class DashboardView(View):
    def get(self, request):
        expenses = Expense.objects.all()
        incomes = Income.objects.all()
        credits_ = Credit.objects.filter(status="active")

        total_incomes_amount = get_total_amount(incomes)
        total_expenses_amount = get_total_amount(expenses)
        total_credits_amount = get_total_amount(credits_)
        wallet_amount = (
            total_incomes_amount - total_expenses_amount - total_credits_amount
        )

        expenses = get_model_with_kind_property(expenses, "Expense")
        incomes = get_model_with_kind_property(incomes, "Income")
        credits_ = get_model_with_kind_property(credits_, "Credit")

        obj_list = get_flatten_lists(expenses, incomes, credits_)
        context = {
            "title": "Dashboard",
            "obj_list": obj_list,
            "total_incomes": total_incomes_amount,
            "total_expenses": total_expenses_amount,
            "total_credits": total_credits_amount,
            "wallet_amount": wallet_amount,
        }
        return render(request, template_name="dashboard/index.html", context=context)
