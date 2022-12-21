from django.test import TestCase

from walletapp.credits.models import Credit

TEST_CONCEPT = "test_concept"
TEST_AMOUNT = 100


def create_test_credit_model() -> Credit:
    return Credit.objects.create(concept=TEST_CONCEPT, amount=TEST_AMOUNT)


class CreditsModelTests(TestCase):
    def test_add_payment_to_credit_with_a_value_greater_than_credit(self):
        credit = create_test_credit_model()

        with self.assertRaises(ValueError) as context:
            credit.add_payment(TEST_AMOUNT + 1)
            exception_message = "The amount is less thant the payment value."
            self.assertEqual(context.exception, exception_message)

    def test_add_payment_to_credit_with_a_correct_value(self):
        credit = create_test_credit_model()
        credit.add_payment(TEST_AMOUNT)
        credit.save()

        credit = Credit.objects.get(pk=credit.pk)

        self.assertLess(credit.amount, TEST_AMOUNT)
