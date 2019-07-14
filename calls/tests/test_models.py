from django.test import TestCase

from ..models import Call, CallStart, CallEnd


class CallTestCase(TestCase):
    def setUp(self):
        self.call = Call(id=70)
        self.call_start = CallStart(timestamp='2016-02-29T12:00:00Z', source='99988526423', destination='9933468278')
        self.call_end = CallEnd(timestamp='2016-02-29T12:00:00Z')

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
        self.call_end.call = self.call

        self.call_end.save()
        new_count = CallEnd.objects.count()

        self.assertNotEqual(old_count, new_count)
