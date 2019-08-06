from datetime import timedelta
from django.test import TestCase

from helpers import date_time_format


class DateTimeFormatTestCase(TestCase):
    def test_should_return_formatted_time_without_days_when_passed_timedelta(self):
        t_delta = timedelta(days=2, hours=3, minutes=21, seconds=53)
        fmt = '{hours}h{minutes}m{seconds}s'
        self.assertEqual(date_time_format.strfdelta(t_delta, fmt), '51h21m53s')
