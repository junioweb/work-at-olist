from django.test import TestCase

from calls.domain.call import Call, CallStart, CallEnd

from bills.domain.bill import CallRecord


class CallRecordTestCase(TestCase):
    def setUp(self):
        first_call = Call.objects.create(id=74)
        CallStart.objects.create(call=first_call, timestamp='2017-12-13T21:57:13Z',
                                 source='99988526423', destination='9933468278')
        CallEnd.objects.create(call=first_call, timestamp='2017-12-14T22:10:56Z')
        self.call = Call.objects.get(id=74)

    def test_should_get_price_when_accessed(self):
        call_record = CallRecord(self.call)
        self.assertEqual(call_record.price, 86.94)
