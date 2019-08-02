import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.models import Call, CallEnd, CallStart


class PutTestCase(APITestCase):
    def setUp(self):
        self.first_call = Call.objects.create(id=101)
        self.second_call = Call.objects.create(id=102)
        self.first_call_start = CallStart.objects.create(call=self.first_call, timestamp='2016-02-29T12:00:00Z',
                                                         source='99988526423', destination='9933468278')
        self.second_call_start = CallStart.objects.create(call=self.second_call, timestamp='2017-12-11T15:07:13Z',
                                                          source='99988526423', destination='9933468278')
        self.valid_payload = {
            'call_id': 101,
            'type': 'start',
            'timestamp': '2016-02-29T12:00:00Z',
            'source': '99988526423',
            'destination': '9933468278',
        }
        self.invalid_payload = {
            'call_id': 102,
            'type': 'start',
            'timestamp': '2016-02-29T12:00:00Z',
            'source': '',
            'destination': '9933468278',
        }

    def test_should_update_call_start_when_passed_valid_payload(self):
        response = self.client.put(
            reverse('calls:start-detail', kwargs={'pk': self.first_call_start.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_bad_request_when_passed_invalid_payload(self):
        response = self.client.put(
            reverse('calls:start-detail', kwargs={'pk': self.first_call_start.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_status_422_and_error_message_when_timestamp_greater_than_end_call_timestamp(self):
        CallEnd.objects.create(call=self.first_call, timestamp='2017-12-11T15:14:56Z')
        payload = {
            'call_id': 101,
            'type': 'start',
            'timestamp': '2017-12-11T15:18:56Z',
            'source': '99988526423',
            'destination': '9933468278',
        }
        response = self.client.put(
            reverse('calls:start-detail', kwargs={'pk': self.first_call_start.pk}),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.data,
                         {'detail': 'Start call timestamp can\'t be greater than the end call timestamp'})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
