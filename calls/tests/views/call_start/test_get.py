from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.domain.call import Call, CallStart
from calls.serializers import CallStartSerializer


class GetTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=96)
        second_call = Call.objects.create(id=97)
        self.first_call_start = CallStart.objects.create(call=first_call, timestamp='2016-02-29T12:00:00Z',
                                                         source='99988526423', destination='9933468278')
        self.second_call_start = CallStart.objects.create(call=second_call, timestamp='2017-12-11T15:07:13Z',
                                                          source='99988526423', destination='9933468278')

    def test_should_get_all_started_calls_when_requested_by_the_client(self):
        response = self.client.get(
            reverse('calls:start-list'))
        started_calls = CallStart.objects.all()
        serializer = CallStartSerializer(started_calls, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_get_valid_single_call_start_when_requested_by_the_client(self):
        response = self.client.get(
            reverse('calls:start-detail', kwargs={'pk': self.first_call_start.pk}))
        call_start = CallStart.objects.get(pk=self.first_call_start.pk)
        serializer = CallStartSerializer(call_start)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_status_code_200_and_empty_data_when_get_invalid_pk(self):
        response = self.client.get(
            reverse('calls:start-detail', kwargs={'pk': 68}))
        self.assertEqual(response.data, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
