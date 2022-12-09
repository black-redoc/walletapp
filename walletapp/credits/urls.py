from django.urls import path

from .views import CreditCreateView, CreditListView, CreditPayView, CreditUpdateView

app_name = "credits"
urlpatterns = [
    path("", CreditListView.as_view(), name="index"),
    path("create/", CreditCreateView.as_view(), name="create"),
    path("update/<int:pk>/", CreditUpdateView.as_view(), name="update"),
    path("pay/<int:pk>/", CreditPayView.as_view(), name="pay"),
]
