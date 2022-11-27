from datetime import datetime

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


# Create your views here.
def index_view(request: HttpRequest, page_number: int) -> HttpResponse:
    current_page = page_number
    page_list = [i for i in range(1, 5)]
    page_count = len(page_list)
    prev_page = page_number - 1
    next_page = page_number + 1
    last_page = page_list[-1]
    incomes = [
        {
            "id": i,
            "concept": "Salary",
            "amount": "500.000,00",
            "created_at": "20/11/2022",
        }
        for i in range(1, 13)
    ]
    total = sum(
        [
            int(income["amount"].replace(".", "").replace(",00", ""))
            for income in incomes
        ]
    )
    total = str(total)
    total = f"{total[0]}.{total[-6:-3]}.{total[-3:]},00"
    context = {
        "title": "Incomes",
        "incomes": incomes,
        "current_page": current_page,
        "page_count": page_count,
        "page_list": page_list,
        "next_page": next_page,
        "prev_page": prev_page,
        "last_page": last_page,
        "total": total
    }
    return render(request, template_name="incomes/index.html", context=context)


def new_income_view(request: HttpRequest) -> HttpRequest:
    current_date = datetime.now()
    current_date = f"{current_date.year}-{current_date.month}-{current_date.day}"
    context = {
        "title": "Create incomes",
        "current_date": current_date,
    }
    return render(request, template_name="incomes/form.html", context=context)


def create_income_view(request: HttpRequest) -> HttpRequest:
    response = ""
    for concept, amount in zip(
        [request.POST.get(f"concept{i}") for i in range(1, 13)],
        [request.POST.get(f"amount{i}") for i in range(1, 13)],
    ):
        if amount is not None or concept is not None:
            response += f"{concept} {amount} "
    return redirect(reverse_lazy("incomes:index"))


def edit_income_view(request: HttpRequest, id: int) -> HttpResponse:
    income = {
        "id": id,
        "concept": "Salary",
        "amount": "5.500.000,00",
        "created_at": "10/10/2022",
    }
    context = {"title": "Update income", "income": income}
    return render(request, template_name="incomes/form.html", context=context)


def update_income_view(request: HttpRequest) -> HttpResponse:
    return redirect(reverse_lazy("incomes:index"))


def delete_incomes_view(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="incomes/delete.html")
