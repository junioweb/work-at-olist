from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.domain.call import Call, CallEnd, CallStart


class DeleteTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=83)
        second_call = Call.objects.create(id=84)
        CallStart.objects.create(call=first_call, timestamp='2016-02-29T12:00:00Z',
                                 source='99988526423', destination='9933468278')
        CallStart.objects.create(call=second_call, timestamp='2017-12-11T15:07:13Z',
                                 source='99988526423', destination='9933468278')
        self.first_call_end = CallEnd.objects.create(call=first_call, timestamp='2016-02-29T14:00:00Z')
        self.second_call_end = CallEnd.objects.create(call=second_call, timestamp='2017-12-11T15:14:56Z')

    def test_should_delete_call_end_when_requested_by_the_client(self):
        response = self.client.delete(
            reverse('calls:end-detail', kwargs={'pk': self.first_call_end.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_status_code_200_and_empty_data_when_delete_invalid_pk(self):
        response = self.client.get(
            reverse('calls:end-detail', kwargs={'pk': 38}))
        self.assertEqual(response.data, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
