import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.domain.call import Call, CallEnd, CallStart


class PatchTestCase(APITestCase):
    def setUp(self):
        self.first_call = Call.objects.create(id=74)
        self.second_call = Call.objects.create(id=75)
        CallStart.objects.create(call=self.first_call, timestamp='2016-02-29T12:00:00Z',
                                 source='99988526423', destination='9933468278')
        CallStart.objects.create(call=self.second_call, timestamp='2017-12-11T15:07:13Z',
                                 source='99988526423', destination='9933468278')
        CallEnd.objects.create(call=self.first_call, timestamp='2016-02-29T14:00:00Z')
        CallEnd.objects.create(call=self.second_call, timestamp='2017-12-11T15:14:56Z')
        self.valid_payload = {
            'records': [
                {
                    'type': 'end',
                    'timestamp': '2016-02-29T13:00:00Z',
                },
            ]
        }
        self.invalid_payload = {
            'records': [
                {
                    'type': 'start',
                    'timestamp': '',
                },
            ]
        }

    def test_should_modify_a_limited_number_of_fields_when_passed_valid_payload(self):
        response = self.client.patch(
            reverse('calls:-detail', kwargs={'pk': self.first_call.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_bad_request_when_passed_invalid_payload(self):
        response = self.client.patch(
            reverse('calls:-detail', kwargs={'pk': self.second_call.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
