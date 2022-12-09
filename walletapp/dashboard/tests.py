from django.test import Client, TestCase
from django.urls import reverse

from walletapp.credits.models import Credit
from walletapp.expenses.models import Expense
from walletapp.incomes.models import Income


class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_empty_database_get_dashboard_on_zeros(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["obj_list"], [])
        self.assertEqual(response.context["total_incomes"], 0)
        self.assertEqual(response.context["total_expenses"], 0)
        self.assertEqual(response.context["total_credits"], 0)
        self.assertEqual(response.context["wallet_amount"], 0)

    def test_full_database_get_dashbord_with_data(self):
        income_amount = 1000
        expense_amount = 500
        credit_amount = 100
        income = Income.objects.create(
            concept="test_1", slug="test_slug_1", amount=income_amount
        )
        expense = Expense.objects.create(
            concept="test_2", slug="test_slug_2", amount=expense_amount
        )
        credit = Credit.objects.create(
            concept="test_3", slug="test_slug_3", amount=credit_amount
        )

        response = self.client.get(reverse("dashboard:index"))
        obj_list = response.context["obj_list"]

        self.assertEqual(response.status_code, 200)
        self.assertIn(income, obj_list)
        self.assertIn(expense, obj_list)
        self.assertIn(credit, obj_list)
        self.assertEqual(response.context["total_incomes"], income.amount)
        self.assertEqual(response.context["total_expenses"], expense.amount)
        self.assertEqual(response.context["total_credits"], credit.amount)
        self.assertEqual(
            response.context["wallet_amount"],
            income_amount - expense_amount - credit_amount,
        )
