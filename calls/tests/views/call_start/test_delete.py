from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.models import Call, CallStart


class DeleteTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=70)
        second_call = Call.objects.create(id=71)
        self.first_call_start = CallStart.objects.create(call=first_call, timestamp='2016-02-29T12:00:00Z',
                                                         source='99988526423', destination='9933468278')
        self.second_call_start = CallStart.objects.create(call=second_call, timestamp='2017-12-11T15:07:13Z',
                                                          source='99988526423', destination='9933468278')

    def test_should_delete_call_start_when_requested_by_the_client(self):
        response = self.client.delete(
            reverse('calls:start-detail', kwargs={'pk': self.first_call_start.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_status_code_200_and_empty_data_when_delete_invalid_pk(self):
        response = self.client.get(
            reverse('calls:start-detail', kwargs={'pk': 27}))
        self.assertEqual(response.data, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
