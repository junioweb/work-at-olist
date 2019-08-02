import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.models import Call, CallStart


class PostTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=89)
        CallStart.objects.create(call=first_call, timestamp='2016-02-29T12:00:00Z',
                                 source='99988526423', destination='9933468278')
        self.valid_payload = {
            'call_id': 89,
            'type': 'end',
            'timestamp': '2016-02-29T14:00:00Z',
        }
        self.invalid_payload = {
            'call_id': 89,
            'type': 'end',
            'timestamp': '',
        }

    def test_should_create_call_end_when_passed_valid_payload(self):
        response = self.client.post(
            reverse('calls:end-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_return_bad_request_when_create_invalid_call_end(self):
        response = self.client.post(
            reverse('calls:end-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_status_422_and_error_message_in_detail_when_create_a_end_call_without_start_call(self):
        Call.objects.create(id=90)
        payload = {
            'call_id': 90,
            'type': 'end',
            'timestamp': '2017-12-11T15:14:56Z',
        }
        response = self.client.post(
            reverse('calls:end-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, {'detail': 'Not allowed to create a end call without a start call'})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_should_return_status_422_and_error_message_when_create_with_timestamp_less_than_start_timestamp(self):
        call = Call.objects.create(id=91)
        CallStart.objects.create(call=call, timestamp='2017-12-11T15:07:13Z', source='99988526423',
                                 destination='9933468278')
        payload = {
            'call_id': 91,
            'type': 'end',
            'timestamp': '2017-12-11T15:05:56Z',
        }
        response = self.client.post(
            reverse('calls:end-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, {'detail': 'End call timestamp can\'t be less than the start call timestamp'})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
