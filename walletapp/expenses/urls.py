from django.urls import path

from walletapp.expenses.views import (
    ExpenseCreateView,
    ExpenseDeleteView,
    ExpenseListView,
    ExpenseUpdateView,
)

app_name = "expenses"
urlpatterns = [
    path("", view=ExpenseListView.as_view(), name="index"),
    path("create/", view=ExpenseCreateView.as_view(), name="create"),
    path("update/<int:pk>/", view=ExpenseUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", view=ExpenseDeleteView.as_view(), name="delete"),
]
