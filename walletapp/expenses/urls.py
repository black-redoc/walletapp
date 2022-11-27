from django.urls import path

from walletapp.expenses.views import (
    index_view
)

app_name = "expenses"
urlpatterns = [
    path("<int:page_number>/", view=index_view, name="index"),
#     path("new/", view=new_income_view, name="new"),
#     path("create/", view=create_income_view, name="create"),
#     path("edit/<int:id>/", view=edit_income_view, name="edit"),
#     path("update/<int:id>/", view=update_income_view, name="update"),
#     path("delete/<int:id>/", view=delete_incomes_view, name="delete"),
]
