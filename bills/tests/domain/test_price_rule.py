from django.test import TestCase

from bills.domain.price_rule import PriceRule


class PriceRuleTestCase(TestCase):
    def test_should_calculate_price_when_passed_the_duration_in_minutes(self):
        price_rule = PriceRule(minute_charge=0.09)
        price = price_rule.calculate_price(duration=8, with_connection=False)
        self.assertEqual(price, 0.72)

    def test_should_calculate_price_with_connection_cost_when_the_flag_with_connection_is_true(self):
        price_rule = PriceRule(minute_charge=0.09, standing_charge=0.36)
        price = price_rule.calculate_price(duration=8, with_connection=True)
        self.assertEqual(price, 1.08)
