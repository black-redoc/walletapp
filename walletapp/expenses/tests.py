from random import randrange
from uuid import uuid4

from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from .models import Expense

MIN_AMOUNT = 1_000
MAX_AMOUNT = 1_000_000
TOTAL_EXPENSES_BY_DEFAULT = 4


class ExpenseListTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.expenses = Expense.objects.bulk_create(
            [
                Expense(
                    concept=str(uuid4()),
                    amount=randrange(MIN_AMOUNT, MAX_AMOUNT),
                )
                for _ in range(TOTAL_EXPENSES_BY_DEFAULT)
            ]
        )

    def test_db_is_not_empty(self):
        self.assertEqual(Expense.objects.all().count(), TOTAL_EXPENSES_BY_DEFAULT)

    def test_load_expense_list_view_then_return_200(self) -> None:
        response = self.client.get(reverse("expenses:index"))
        expeted_status = 200
        self.assertEqual(response.status_code, expeted_status)

    def test_load_expense_create_form_then_return_200(self) -> None:
        response = self.client.get(reverse("expenses:create"))
        expeted_status = 200
        self.assertEqual(response.status_code, expeted_status)

    def test_create_new_expense_then_return_new_expense(self):
        concept_expected = "new concept"
        amount_expected = 1_000_000
        data = {"concept": concept_expected, "amount": amount_expected}
        response = self.client.post(reverse("expenses:create"), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), TOTAL_EXPENSES_BY_DEFAULT + 1)

        obj = Expense.objects.last()
        self.assertEqual(obj.concept, concept_expected)
        self.assertEqual(obj.amount, amount_expected)

    def test_load_expense_edit_form_then_return_200(self) -> None:
        obj = self.expenses[0]
        response = self.client.get(reverse("expenses:update", kwargs={"pk": obj.pk}))
        expeted_status = 200
        self.assertEqual(response.status_code, expeted_status)

    def test_load_expense_edit_form_with_non_existent_pk_then_return_404(self):
        non_existent_pk = 123
        response = self.client.get(
            reverse("expenses:update", kwargs={"pk": non_existent_pk})
        )
        expected_status = 404
        self.assertEqual(response.status_code, expected_status)

    def test_update_existent_expense_then_return_new_expense(self) -> None:
        obj = self.expenses[0]
        data = {"concept": "updated concept", "amount": 123}
        response = self.client.post(
            reverse("expenses:update", kwargs={"pk": obj.pk}), data=data
        )

        messages = list(get_messages(response.wsgi_request))
        message_expected = "Expense was updated successfully!"

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), message_expected)

    def test_update_non_existent_expense_then_return_404(self):
        non_existent_pk = 123
        data = {}

        response = self.client.post(
            reverse("expenses:update", kwargs={"pk": non_existent_pk}), data=data
        )

        self.assertEqual(response.status_code, 404)

    def test_update_existent_expense_with_invalid_data_then_return_error_message(self):
        obj = self.expenses[0]
        data = {}

        response = self.client.post(
            reverse("expenses:update", kwargs={"pk": obj.pk}), data=data
        )

        messages = list(get_messages(response.wsgi_request))
        message_expected = "Form is not valid!"

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), message_expected)

    def test_load_expense_delete_form_then_return_200(self) -> None:
        obj = self.expenses[0]
        response = self.client.get(reverse("expenses:delete", kwargs={"pk": obj.pk}))
        expeted_status = 200
        self.assertEqual(response.status_code, expeted_status)

    def test_load_non_exisent_expense_delete_form_then_return_404(self) -> None:
        non_existent_pk = 123
        response = self.client.get(
            reverse("expenses:delete", kwargs={"pk": non_existent_pk})
        )
        expeted_status = 404
        self.assertEqual(response.status_code, expeted_status)

    def test_delete_existent_expense_then_return_success(self):
        obj = self.expenses[0]
        response = self.client.post(reverse("expenses:delete", kwargs={"pk": obj.pk}))
        messages = list(get_messages(response.wsgi_request))
        message_expected = "Expense was deleted successfully!"

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), message_expected)

    def test_delete_non_existent_expense_then_return_404(self):
        non_existent_pk = 123
        response = self.client.post(
            reverse("expenses:delete", kwargs={"pk": non_existent_pk})
        )

        self.assertEqual(response.status_code, 404)
