from django.contrib.messages import get_messages
from django.shortcuts import reverse
from django.test import TestCase, Client

from walletapp.credits.models import Credit

TOTAL_CREDITS_COUNT = 3


class CreditViewTests(TestCase):
    def setUp(self):
        TEST_CONCEPT = "test_concept_"
        TEST_AMOUNT = 100
        TEST_SLUG = "test_slug_"
        self.client = Client()
        self.credits = [
            Credit(
                concept=TEST_CONCEPT + str(i),
                slug=TEST_SLUG + str(i),
                amount=TEST_AMOUNT,
            )
            for i in range(TOTAL_CREDITS_COUNT)
        ]
        Credit.objects.bulk_create(self.credits)

    def test_load_credit_list_view_then_return_200(self):
        response = self.client.get(reverse("credits:index"))
        obj_list = response.context["object_list"]
        expected_credit = self.credits[0]

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_credit, obj_list)

    def test_create_new_credit_then_return_new_credit(self):
        concept_expected = "concept1"
        data = {
            "concept": concept_expected,
            "amount": 1000,
        }
        response = self.client.post(reverse("credits:create"), data)
        messages = [
            str(message) for message in list(get_messages(response.wsgi_request))
        ]
        credit = Credit.objects.filter(concept=concept_expected)

        self.assertEqual(response.status_code, 302)
        self.assertIn("Credit was created successfully!", messages)
        self.assertIsNotNone(credit)

    def test_pay_credit_then_return_reduced_credit_amount(self):
        payment = 50
        pk = self.credits[0].pk
        amount = self.credits[0].amount
        data = {"payment": payment}

        response = self.client.post(reverse("credits:pay", kwargs={"pk": pk}), data)
        messages = [
            str(message) for message in list(get_messages(response.wsgi_request))
        ]

        self.assertEqual(response.status_code, 302)
        self.assertIn("Added payment to credit!", messages)
        credit = Credit.objects.get(pk=pk)
        self.assertEqual(credit.amount, amount - payment)

    def test_update_get_existent_credit_view_then_return_a_credit(self):
        credit = self.credits[0]
        response = self.client.get(reverse("credits:update", kwargs={"pk": credit.pk}))

        obj = response.context["credit"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(obj, credit)

    def test_update_nonexistent_credit_then_return_404(self):
        non_existent_pk = 123456
        response = self.client.get(reverse("credits:update", kwargs={"pk": non_existent_pk}))

        self.assertEqual(response.status_code, 404)

    def test_update_credit_then_return_updated_credit(self):
        pk = self.credits[0].pk
        old_concept = self.credits[0].concept
        old_amount = self.credits[0].amount
        expected_concept = "updated_credit"
        expected_amount = 123
        data = {"concept": expected_concept, "amount": expected_amount}

        response = self.client.post(reverse("credits:update", kwargs={"pk": pk}), data)
        messages = [
            str(message) for message in list(get_messages(response.wsgi_request))
        ]
        credit = Credit.objects.get(pk=pk)

        self.assertEqual(response.status_code, 302)
        self.assertIn("Credit was updated successfully!", messages)
        self.assertEqual(credit.concept, expected_concept)
        self.assertEqual(credit.amount, expected_amount)
        self.assertNotEqual(credit.concept, old_concept)
        self.assertNotEqual(credit.amount, old_amount)
