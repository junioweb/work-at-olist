import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.models import Call, CallStart


class PutCallStartTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=70)
        second_call = Call.objects.create(id=71)
        self.first_call_start = CallStart.objects.create(call=first_call, timestamp='2016-02-29T12:00:00Z',
                                                         source='99988526423', destination='9933468278')
        self.second_call_start = CallStart.objects.create(call=second_call, timestamp='2017-12-11T15:07:13Z',
                                                          source='99988526423', destination='9933468278')
        self.valid_payload = {
            'call_id': 70,
            'timestamp': '2016-02-29T12:00:00Z',
            'source': '99988526423',
            'destination': '9933468278',
        }
        self.invalid_payload = {
            'call_id': 70,
            'timestamp': '2016-02-29T12:00:00Z',
            'source': '',
            'destination': '9933468278',
        }

    def test_should_create_call_start_when_passed_valid_payload(self):
        response = self.client.put(
            reverse('calls:start-detail', kwargs={'pk': self.first_call_start.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_bad_request_when_create_invalid_call_start(self):
        response = self.client.put(
            reverse('calls:start-detail', kwargs={'pk': self.first_call_start.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
