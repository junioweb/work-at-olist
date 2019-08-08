from django.test import TestCase

from calls.domain.call import Call, CallStart, CallEnd

from bills.domain.bill import Bill
from bills.exceptions import CallDifferentPeriodsError, CallDifferentSubscribersError


class BillTestCase(TestCase):
    def setUp(self):
        self.first_call = Call.objects.create(id=74)
        CallStart.objects.create(call=self.first_call, timestamp='2017-12-12T04:57:13Z',
                                 source='99988526423', destination='9933468278')
        CallEnd.objects.create(call=self.first_call, timestamp='2017-12-12T06:10:56Z')

        self.second_call = Call.objects.create(id=75)
        CallStart.objects.create(call=self.second_call, timestamp='2017-12-13T21:57:13Z',
                                 source='99988526423', destination='9933468278')
        CallEnd.objects.create(call=self.second_call, timestamp='2017-12-14T22:10:56Z')

        self.calls = Call.objects.filter(id__in=[self.first_call.id, self.second_call.id])
        self.bill = Bill(self.calls)

    def test_should_return_the_subscriber_when_accessed(self):
        self.assertEqual(self.bill.subscriber, self.calls[0].start.source)

    def test_should_return_the_period_when_accessed(self):
        period = '{}/{}'.format(self.calls[0].end.timestamp.month, self.calls[0].end.timestamp.year)
        self.assertEqual(self.bill.period, period)

    def test_should_return_the_total_when_accessed(self):
        self.assertEqual(self.bill.total, 88.20)

    def test_should_throw_exception_when_create_bill_instance_with_call_different_periods(self):
        call = Call.objects.create(id=77)
        CallStart.objects.create(call=call, timestamp='2018-02-28T21:57:13Z',
                                 source='99988526423', destination='9933468278')
        CallEnd.objects.create(call=call, timestamp='2018-03-01T22:10:56Z')
        calls = Call.objects.filter(id__in=[self.first_call.id, self.second_call.id, call.id])

        with self.assertRaises(CallDifferentPeriodsError):
            Bill(calls)

    def test_should_throw_exception_when_create_bill_instance_with_call_different_subscribers(self):
        call = Call.objects.create(id=76)
        CallStart.objects.create(call=call, timestamp='2017-12-12T15:07:58Z',
                                 source='99988526415', destination='9933468278')
        CallEnd.objects.create(call=call, timestamp='2017-12-12T15:12:56Z')
        calls = Call.objects.filter(id__in=[self.first_call.id, self.second_call.id, call.id])

        with self.assertRaises(CallDifferentSubscribersError):
            Bill(calls)
