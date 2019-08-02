from django.db import IntegrityError
from django.test import TestCase

from calls.models import Call, CallStart, CallEnd


class CallTestCase(TestCase):
    def setUp(self):
        self.call = Call(id=69)

    def test_should_be_able_to_create_a_call_when_saving_the_object(self):
        old_count = Call.objects.count()
        self.call.save()
        new_count = Call.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_should_throw_exception_when_a_call_record_pair_already_exists(self):
        self.call.save()
        CallStart.objects.create(call=self.call, timestamp='2016-02-29T12:00:00Z', source='99988526423',
                                 destination='9933468278')
        CallEnd.objects.create(call=self.call, timestamp='2016-02-29T14:00:00Z')

        with self.assertRaises(IntegrityError):
            CallEnd.objects.create(call=self.call, timestamp='2016-02-29T15:00:00Z')
