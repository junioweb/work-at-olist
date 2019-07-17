import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.models import Call, CallStart


class PostTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=70)
        CallStart.objects.create(call=first_call, timestamp='2016-02-29T12:00:00Z',
                                 source='99988526423', destination='9933468278')
        self.valid_payload = {
            'call_id': 70,
            'timestamp': '2016-02-29T14:00:00Z',
        }
        self.invalid_payload = {
            'call_id': 70,
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
