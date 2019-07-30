from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.models import Call, CallEnd, CallStart


class DeleteTestCase(APITestCase):
    def setUp(self):
        self.first_call = Call.objects.create(id=70)
        self.second_call = Call.objects.create(id=71)
        CallStart.objects.create(call=self.first_call, timestamp='2016-02-29T12:00:00Z',
                                 source='99988526423', destination='9933468278')
        CallStart.objects.create(call=self.second_call, timestamp='2017-12-11T15:07:13Z',
                                 source='99988526423', destination='9933468278')
        CallEnd.objects.create(call=self.first_call, timestamp='2016-02-29T14:00:00Z')
        CallEnd.objects.create(call=self.second_call, timestamp='2017-12-11T15:14:56Z')

    def test_should_delete_call_when_requested_by_the_client(self):
        response = self.client.delete(
            reverse('calls:-detail', kwargs={'pk': self.first_call.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_delete_call_records_when_delete_a_call(self):
        response = self.client.delete(
            reverse('calls:-detail', kwargs={'pk': self.first_call.pk}))
        has_call_start = CallStart.objects.filter(call_id=self.first_call.pk).exists()
        has_call_end = CallEnd.objects.filter(call_id=self.first_call.pk).exists()
        self.assertEqual(has_call_start & has_call_end, False)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_status_code_200_and_empty_data_when_delete_invalid_pk(self):
        response = self.client.get(
            reverse('calls:-detail', kwargs={'pk': 27}))
        self.assertEqual(response.data, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
