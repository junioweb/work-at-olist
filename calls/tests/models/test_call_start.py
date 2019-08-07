from django.test import TestCase

from calls.exceptions import TimestampGreaterThanCallEndTimestampError

from calls.domain.call import Call, CallStart, CallEnd


class CallStartTestCase(TestCase):
    def setUp(self):
        self.call = Call.objects.create(id=67)
        self.call_start = CallStart(call=self.call, timestamp='2016-02-29T12:00:00Z', source='99988526423',
                                    destination='9933468278')

    def test_should_be_able_to_create_a_start_call_when_saving_the_object(self):
        old_count = CallStart.objects.count()
        self.call_start.save()
        new_count = CallStart.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_should_throw_exception_when_update_a_start_call_to_timestamp_greater_than_end_call_timestamp(self):
        self.call_start.save()
        CallEnd(call=self.call, timestamp='2016-02-29T14:00:00Z')

        with self.assertRaises(TimestampGreaterThanCallEndTimestampError):
            self.call_start.timestamp = '2016-02-29T15:00:00Z'
            self.call_start.save()
