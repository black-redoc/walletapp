from datetime import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import IncomeForm
from .models import Income

MAX_ITEMS_PER_PAGE = 10


def index_view(request: HttpRequest, page_number: int) -> HttpResponse:
    queryset = Income.objects.all().order_by("-pk")
    paginator = Paginator(queryset, MAX_ITEMS_PER_PAGE)
    page_obj = paginator.page(page_number)
    object_list = page_obj.object_list
    total_amount = (
        queryset.only("amount").aggregate(Sum("amount")).get("amount__sum", 0)
    )
    total_paginated = (
        object_list.only("amount").aggregate(Sum("amount")).get("amount__sum", 0)
    )

    context = {
        "page_obj": page_obj,
        "object_list": object_list,
        "title": "Incomes",
        "total_amount": total_amount,
        "total_paginated": total_paginated,
        "paginator": paginator,
    }
    return render(request, template_name="incomes/index.html", context=context)


def new_income_view(request: HttpRequest) -> HttpRequest:
    current_date = datetime.now()
    current_date = current_date.strftime("%Y-%m-%d")
    context = {
        "title": "Create incomes",
        "current_date": current_date,
    }
    return render(request, template_name="incomes/form.html", context=context)


def create_income_view(request: HttpRequest) -> HttpRequest:
    if not request.method == "POST":
        return redirect(reverse("incomes:new", kwargs={"page_number": 1}))

    forms = [
        IncomeForm(dict(concept=concept, amount=amount))
        for concept, amount in zip(
            request.POST.getlist("concept"),
            request.POST.getlist("amount"),
        )
    ]
    if not all(form.is_valid for form in forms):
        messages.error(request, message="Form is not valid!")
        return redirect(reverse("incomes:new"))

    for form in forms:
        form.save()

    if len(forms) > 1:
        messages.success(request, message="Expenses were created successfully")
    else:
        messages.success(request, message="Expense was created successfully")
    return redirect(reverse("incomes:index", kwargs={"page_number": 1}))


def edit_income_view(request: HttpRequest, pk: int) -> HttpResponse:
    income = get_object_or_404(Income, pk=pk)

    context = {"title": "Update income", "income": income}
    return render(request, template_name="incomes/form.html", context=context)


def update_income_view(request: HttpRequest, pk: int) -> HttpResponse:
    income = get_object_or_404(Income, pk=pk)

    if not request.method == "POST":
        return redirect(reverse("incomes:index", kwargs={"page_number": 1}))

    form = IncomeForm(request.POST, instance=income)

    if not form.is_valid():
        messages.error(request, message="Form is not valid!")
        return redirect(reverse("incomes:edit", kwargs={"pk": pk}))

    form.save()

    messages.success(request, message="Income was updated successfully!")
    return redirect(reverse("incomes:index", kwargs={"page_number": 1}))


def delete_incomes_view(request: HttpRequest, pk: int) -> HttpResponse:
    income = get_object_or_404(Income, pk=pk)

    if request.method == "POST":
        income.delete()
        messages.success(request, message="Income was deleted successfully!")
        return redirect(reverse("incomes:index", kwargs={"page_number": 1}))

    context = {
        "object": income,
    }
    return render(request, template_name="incomes/delete.html", context=context)
