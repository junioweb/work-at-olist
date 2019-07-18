from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.models import Call, CallEnd, CallStart
from calls.serializers import CallSerializer


class GetTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=70)
        second_call = Call.objects.create(id=71)
        self.first_call_start = CallStart.objects.create(call=first_call, timestamp='2016-02-29T12:00:00Z',
                                                         source='99988526423', destination='9933468278')
        self.second_call_start = CallStart.objects.create(call=second_call, timestamp='2017-12-11T15:07:13Z',
                                                          source='99988526423', destination='9933468278')
        self.first_call_end = CallEnd.objects.create(call=first_call, timestamp='2016-02-29T14:00:00Z')
        self.second_call_end = CallEnd.objects.create(call=second_call, timestamp='2017-12-11T15:14:56Z')

    def test_should_get_all_calls_when_requested_by_the_client(self):
        response = self.client.get(
            reverse('calls:-list'))
        calls = Call.objects.all()
        serializer = CallSerializer(calls, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
