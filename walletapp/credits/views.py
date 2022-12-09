from datetime import datetime
from typing import Any

from django.contrib import messages
from django.db.models import Sum
from django.http import Http404, HttpRequest
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.urls import reverse
from django.db.models.manager import BaseManager
from django.views.generic import CreateView, ListView, UpdateView

from .forms import CreditForm
from .models import Credit

MAX_ITEMS_PER_PAGE = 10


class CreditListView(ListView):
    model = Credit
    template_name = "credits/index.html"
    paginate_by = MAX_ITEMS_PER_PAGE

    def get_queryset(self) -> BaseManager[Credit]:
        return Credit.objects.filter(status="active")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        total_amount = (
            queryset.only("amount").aggregate(Sum("amount")).get("amount__sum", 0)
        )
        _, _, queryset, _ = self.paginate_queryset(queryset, MAX_ITEMS_PER_PAGE)
        total_amount_per_page = queryset.only("amount").aggregate(Sum("amount"))
        total_amount_per_page = total_amount_per_page.get("amount__sum", 0)
        context.update(
            title="Credits",
            total_amount_per_page=total_amount_per_page,
            total_amount=total_amount,
        )
        return context


class CreditCreateView(CreateView):
    model = Credit
    template_name = "credits/form.html"
    form_class = CreditForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(CreditCreateView, self).get_context_data(**kwargs)
        current_date = datetime.now().strftime("%Y-%m-%d")
        context.update(title="Create credit", current_date=current_date)
        return context

    def get_success_url(self) -> str:
        messages.success(self.request, message="Credit was created successfully!")
        return reverse("credits:index")


class CreditUpdateView(UpdateView):
    model = Credit
    template_name = "credits/form.html"
    queryset = Credit.objects.filter(status="active")
    form_class = CreditForm

    def get_success_url(self) -> str:
        messages.success(self.request, message="Credit was updated successfully!")
        return reverse("credits:index")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(UpdateView, self).get_context_data(**kwargs)
        context.update(title="Update credit")
        return context


class CreditPayView(UpdateView):
    model = Credit
    template_name = "credits/pay_credit_form.html"
    queryset = Credit.objects.filter(status="active")
    form_class = CreditForm

    def post(self, request: HttpRequest, pk: int):
        credit = get_object_or_404(Credit, pk=pk)
        payment_value = request.POST.get("payment", 0)

        credit.amount -= int(payment_value)
        credit.save()

        messages.success(request, message="Added payment to credit!")
        return redirect(reverse("credits:index"))

    def get_success_url(self) -> str:
        messages.success(self.request, message="Added payment to credit successfully!")
        return reverse("credits:index")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(UpdateView, self).get_context_data(**kwargs)
        context.update(title="Pay credit")
        return context
