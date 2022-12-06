from django.test import Client, TestCase
from django.urls import reverse

from walletapp.expenses.models import Expense
from walletapp.incomes.models import Income


class TestDashboardView(TestCase):
    def setUp(self):
        self.client = Client()

    def empty_database_get_dashboard_on_zeros_test(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["obj_list"], [])
        self.assertEqual(response.context["total_incomes"], 0)
        self.assertEqual(response.context["total_expenses"], 0)
        self.assertEqual(response.context["wallet_amount"], 0)

    def full_database_get_dashbord_with_data_test(self):
        income_amount = 1000
        expense_amount = 500
        income = Income.objects.create(
            concept="test_1", slug="test_slug_1", amount=income_amount
        )
        expense = Expense.objects.create(
            concept="test_2", slug="test_slug_2", amount=expense_amount
        )

        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["obj_list"], [income, expense])
        self.assertEqual(response.context["total_incomes"], income.amount)
        self.assertEqual(response.context["total_expenses"], expense.amount)
        self.assertEqual(
            response.context["wallet_amount"], income_amount - expense_amount
        )
