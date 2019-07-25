import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PostTestCase(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'call_id': 70,
            'records': [
                {
                    'type': 'start',
                    'timestamp': '2016-02-29T12:00:00Z',
                    'source': '99988526423',
                    'destination': '9933468278',
                },
            ]
        }
        self.invalid_payload = {
            'call_id': 71,
            'records': [
                {
                    'type': 'start',
                    'timestamp': '2016-02-29T12:00:00Z',
                    'source': '',
                    'destination': '9933468278',
                },
            ]
        }

    def test_should_create_call_when_passed_valid_payload(self):
        response = self.client.post(
            reverse('calls:-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_return_bad_request_when_create_invalid_call(self):
        response = self.client.post(
            reverse('calls:-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
