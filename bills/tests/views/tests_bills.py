from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from calls.domain.call import Call, CallEnd, CallStart
from bills.serializers import BillSerializer


class BillTestCase(APITestCase):
    def setUp(self):
        first_call = Call.objects.create(id=72)
        second_call = Call.objects.create(id=73)
        CallStart.objects.create(call=first_call, timestamp='2017-12-12T22:47:56Z',
                                 source='99988526423', destination='9933468278')
        CallStart.objects.create(call=second_call, timestamp='2017-12-12T21:57:13Z',
                                 source='99988526423', destination='9933468278')
        CallEnd.objects.create(call=first_call, timestamp='2017-12-12T22:50:56Z')
        CallEnd.objects.create(call=second_call, timestamp='2017-12-12T22:10:56Z')

    def test_should_get_bill_when_requested_with_subscriber_telephone_number(self):
        response = self.client.get(
            reverse('bills:bills') + '?subscriber=99988526423')
        calls = Call.objects.filter(start__source='99988526423')
        serializer = BillSerializer(calls)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_status_code_200_and_empty_data_when_subscriber_not_exist(self):
        response = self.client.get(
            reverse('bills:bills') + '?subscriber=99988526768')

        self.assertEqual(response.data, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_status_422_and_error_message_when_subscriber_not_passed(self):
        response = self.client.get(reverse('bills:bills'))

        self.assertEqual(response.data, {'detail': 'Not allowed to get bills when subscriber not informed'})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_should_get_bill_when_requested_with_subscriber_and_period(self):
        call = Call.objects.create(id=70)
        CallStart.objects.create(call=call, timestamp='2016-02-29T12:00:00Z',
                                 source='99988526423', destination='9933468278')
        CallEnd.objects.create(call=call, timestamp='2016-02-29T14:00:00Z')

        response = self.client.get(
            reverse('bills:bills') + '?subscriber=99988526423&period=02/2016')
        calls = Call.objects.filter(start__source='99988526423', end__timestamp__month=2,
                                    end__timestamp__year=2016)
        serializer = BillSerializer(calls)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
