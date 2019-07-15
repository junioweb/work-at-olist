from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from ..models import Call, CallStart, CallEnd


class CallTestCase(TestCase):
    def setUp(self):
        self.call = Call(id=70)
        self.call_start = CallStart(timestamp='2016-02-29T12:00:00Z', source='99988526423', destination='9933468278')
        self.call_end = CallEnd(timestamp='2016-02-29T14:00:00Z')

    def test_should_be_able_to_create_a_call_when_saving_the_object(self):
        old_count = Call.objects.count()
        self.call.save()
        new_count = Call.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_should_be_able_to_create_a_start_call_when_saving_the_object(self):
        old_count = CallStart.objects.count()
        self.call.save()

        self.call_start.call = self.call
        self.call_start.save()
        new_count = CallStart.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_should_be_able_to_create_a_end_call_when_saving_the_object(self):
        old_count = CallEnd.objects.count()
        self.call.save()
        self.call_start.call = self.call
        self.call_start.save()

        self.call_end.call = self.call
        self.call_end.save()
        new_count = CallEnd.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_should_throw_exception_when_a_call_record_pair_already_exists(self):
        self.call.save()
        self.call_start.call = self.call
        self.call_start.save()
        self.call_end.call = self.call
        self.call_end.save()

        with self.assertRaises(IntegrityError):
            CallEnd.objects.create(timestamp='2016-02-29T15:00:00Z', call=self.call)

    def test_should_throw_exception_when_create_a_end_call_without_start_call(self):
        self.call.save()
        self.call_end.call = self.call

        with self.assertRaises(ValidationError):
            self.call_end.save()

    def test_should_throw_exception_when_create_a_end_call_with_timestamp_less_than_start_call_timestamp(self):
        self.call.save()
        self.call_start.call = self.call
        self.call_start.save()

        with self.assertRaises(ValueError):
            CallEnd.objects.create(timestamp='2016-02-29T11:00:00Z', call=self.call)

    def test_should_throw_exception_when_update_a_start_call_to_timestamp_greater_than_end_call_timestamp(self):
        self.call.save()
        self.call_start.call = self.call
        self.call_start.save()
        self.call_end.call = self.call
        self.call_end.save()

        with self.assertRaises(ValueError):
            self.call_start.timestamp = '2016-02-29T15:00:00Z'
            self.call_start.save()
