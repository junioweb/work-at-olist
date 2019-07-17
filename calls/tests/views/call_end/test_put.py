import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.models import Call, CallEnd, CallStart


class PutTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=70)
        second_call = Call.objects.create(id=71)
        CallStart.objects.create(call=first_call, timestamp='2016-02-29T12:00:00Z',
                                 source='99988526423', destination='9933468278')
        CallStart.objects.create(call=second_call, timestamp='2017-12-11T15:07:13Z',
                                 source='99988526423', destination='9933468278')
        self.first_call_end = CallEnd.objects.create(call=first_call, timestamp='2016-02-29T14:00:00Z')
        self.second_call_end = CallEnd.objects.create(call=second_call, timestamp='2017-12-11T15:14:56Z')
        self.valid_payload = {
            'call_id': 70,
            'timestamp': '2016-02-29T13:00:00Z',
        }
        self.invalid_payload = {
            'call_id': 71,
            'timestamp': '',
        }

    def test_should_update_call_end_when_passed_valid_payload(self):
        response = self.client.put(
            reverse('calls:end-detail', kwargs={'pk': self.first_call_end.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_return_bad_request_when_passed_invalid_payload(self):
        response = self.client.put(
            reverse('calls:end-detail', kwargs={'pk': self.second_call_end.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
