from django.test import TestCase

from calls.exceptions import CallStartMissingError, TimestampLessThanCallStartTimestampError

from calls.domain.call import Call, CallStart, CallEnd


class CallEndTestCase(TestCase):
    def setUp(self):
        self.call = Call.objects.create(id=68)
        self.call_end = CallEnd(call=self.call, timestamp='2016-02-29T14:00:00Z')

    def test_should_be_able_to_create_a_end_call_when_saving_the_object(self):
        CallStart.objects.create(call=self.call, timestamp='2016-02-29T12:00:00Z', source='99988526423',
                                 destination='9933468278')
        old_count = CallEnd.objects.count()
        self.call_end.save()
        new_count = CallEnd.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_should_throw_exception_when_create_a_end_call_without_start_call(self):
        with self.assertRaises(CallStartMissingError):
            self.call_end.save()

    def test_should_throw_exception_when_create_a_end_call_with_timestamp_less_than_start_call_timestamp(self):
        CallStart.objects.create(call=self.call, timestamp='2016-02-29T12:00:00Z', source='99988526423',
                                 destination='9933468278')

        with self.assertRaises(TimestampLessThanCallStartTimestampError):
            CallEnd.objects.create(timestamp='2016-02-29T11:00:00Z', call=self.call)
