from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.domain.call import Call, CallEnd, CallStart
from calls.serializers import CallEndSerializer


class GetTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=85)
        second_call = Call.objects.create(id=86)
        CallStart.objects.create(call=first_call, timestamp='2016-02-29T12:00:00Z',
                                 source='99988526423', destination='9933468278')
        CallStart.objects.create(call=second_call, timestamp='2017-12-11T15:07:13Z',
                                 source='99988526423', destination='9933468278')
        self.first_call_end = CallEnd.objects.create(call=first_call, timestamp='2016-02-29T14:00:00Z')
        self.second_call_end = CallEnd.objects.create(call=second_call, timestamp='2017-12-11T15:14:56Z')

    def test_should_get_all_ended_calls_when_requested_by_the_client(self):
        response = self.client.get(
            reverse('calls:end-list'))
        ended_calls = CallEnd.objects.all()
        serializer = CallEndSerializer(ended_calls, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_get_valid_single_call_end_when_requested_by_the_client(self):
        response = self.client.get(
            reverse('calls:end-detail', kwargs={'pk': self.first_call_end.pk}))
        call_end = CallEnd.objects.get(pk=self.first_call_end.pk)
        serializer = CallEndSerializer(call_end)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_status_code_200_and_empty_data_when_get_invalid_pk(self):
        response = self.client.get(
            reverse('calls:end-detail', kwargs={'pk': 48}))
        self.assertEqual(response.data, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
