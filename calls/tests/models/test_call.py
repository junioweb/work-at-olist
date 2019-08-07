from django.test import TestCase

from calls.domain.call import Call


class CallTestCase(TestCase):
    def test_should_be_able_to_create_a_call_when_saving_the_object(self):
        old_count = Call.objects.count()
        Call.objects.create(id=69)
        new_count = Call.objects.count()

        self.assertNotEqual(old_count, new_count)
