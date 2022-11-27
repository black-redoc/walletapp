from django.urls import path

from walletapp.incomes.views import (
    create_income_view,
    delete_incomes_view,
    edit_income_view,
    index_view,
    new_income_view,
    update_income_view,
)

app_name = "users"
urlpatterns = [
    path("<int:page_number>/", view=index_view, name="index"),
    path("new/", view=new_income_view, name="new"),
    path("create/", view=create_income_view, name="create"),
    path("edit/<int:id>/", view=edit_income_view, name="edit"),
    path("update/<int:id>/", view=update_income_view, name="update"),
    path("delete/<int:id>/", view=delete_incomes_view, name="delete"),
]
