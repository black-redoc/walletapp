from datetime import datetime
from typing import Any, Dict

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ExpenseForm
from .models import Expense


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/index.html"
    paginate_by = 10
    queryset = Expense.objects.all().order_by("-pk")

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        total_amount = (
            queryset.only("amount").aggregate(Sum("amount")).get("amount__sum", 0)
        )
        _, _, queryset, _ = self.paginate_queryset(queryset, 10)
        total_paginated = queryset.only("amount").aggregate(Sum("amount"))
        total_paginated = total_paginated.get("amount__sum", 0)
        context.update(
            title="Expenses", total_paginated=total_paginated, total_amount=total_amount
        )
        return context


class ExpenseCreateView(CreateView):
    model = Expense
    fields = ["concept", "amount"]
    success_url = reverse_lazy("expenses:index", kwargs={"page_number": 1})

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        current_date = datetime.now()
        current_date = f"{current_date.year}-{current_date.month}-{current_date.day}"
        context.update(title="Create expenses", current_date=current_date)
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        forms = [
            ExpenseForm(dict(concept=concept, amount=amount))
            for concept, amount in zip(
                request.POST.getlist("concept"), request.POST.getlist("amount")
            )
        ]
        if not all(form.is_valid() for form in forms):
            messages.error(request, message="Form is not valid!")
            return redirect(reverse("expenses:create"))

        for form in forms:
            form.save()

        if len(forms) > 1:
            messages.success(request, message="Expenses were created successfully")
        else:
            messages.success(request, message="Expense was created successfully")
        return redirect(reverse("expenses:index"))


class ExpenseUpdateView(UpdateView):
    model = Expense
    template_name = "expenses/expense_update_form.html"
    success_url = reverse_lazy("expenses:index")
    form_class = ExpenseForm

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(title="Update expense")
        return context


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expenses/confirm_delete.html"
    success_url = reverse_lazy("expenses:index")
