from django.test import TestCase

from ..models import Call, CallStart


class CallTestCase(TestCase):
    def setUp(self):
        self.call = Call.objects.create(id=70)
        self.call_start = CallStart(timestamp='2016-02-29T12:00:00Z', call=self.call,
                                    source='99988526423', destination='9933468278')

    def test_should_be_able_to_create_a_start_call_when_saving_the_object(self):
        old_count = Call.objects.filter(start__isnull=False).count()
        self.call_start.save()
        new_count = Call.objects.filter(start__isnull=False).count()
        self.assertNotEqual(old_count, new_count)
