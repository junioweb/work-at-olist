from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.domain.call import Call, CallEnd, CallStart
from calls.serializers import CallSerializer


class GetTestCase(APITestCase):
    def setUp(self):
        self.first_call = Call.objects.create(id=72)
        self.second_call = Call.objects.create(id=73)
        CallStart.objects.create(call=self.first_call, timestamp='2016-02-29T12:00:00Z',
                                 source='99988526423', destination='9933468278')
        CallStart.objects.create(call=self.second_call, timestamp='2017-12-11T15:07:13Z',
                                 source='99988526423', destination='9933468278')
        CallEnd.objects.create(call=self.first_call, timestamp='2016-02-29T14:00:00Z')
        CallEnd.objects.create(call=self.second_call, timestamp='2017-12-11T15:14:56Z')

    def test_should_get_all_calls_when_requested_by_the_client(self):
        response = self.client.get(
            reverse('calls:-list'))
        calls = Call.objects.all()
        serializer = CallSerializer(calls, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_get_valid_single_call_when_requested_by_the_client(self):
        response = self.client.get(
            reverse('calls:-detail', kwargs={'pk': self.first_call.pk}))
        call = Call.objects.get(pk=self.first_call.pk)
        serializer = CallSerializer(call)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_status_code_200_and_empty_data_when_get_invalid_pk(self):
        response = self.client.get(
            reverse('calls:-detail', kwargs={'pk': 28}))
        self.assertEqual(response.data, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
