from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, status
from rest_framework.response import Response

from calls.domain.call import Call, CallEnd

from bills.domain.bill import Bill
from bills.serializers import BillSerializer
from bills.exceptions import SubscriberNotPassedError


class BillViewSet(viewsets.ViewSet):
    """
    retrieve: Return call bill
    """
    subscriber_param = openapi.Parameter('subscriber', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
    period_param = openapi.Parameter('period', openapi.IN_QUERY, description='mm/yyyy', type=openapi.TYPE_STRING)

    @swagger_auto_schema(
        manual_parameters=[subscriber_param, period_param],
        responses={
            '200': BillSerializer,
            '422': 'Not allowed to get bills when subscriber not informed.'
        }
    )
    def retrieve(self, request):
        period = request.query_params.get('period')
        subscriber = request.query_params.get('subscriber')
        if subscriber is None:
            raise SubscriberNotPassedError()
        if period is None:
            last_call_end = CallEnd.objects.all().order_by('-id')[0]
            month = last_call_end.timestamp.month
            year = last_call_end.timestamp.year
        else:
            month, year = period.split('/')

        calls = Call.objects.prefetch_related('start', 'end')
        calls = calls.filter(start__source=subscriber, end__timestamp__month=month, end__timestamp__year=year)
        if not calls.exists():
            return Response({}, status=status.HTTP_200_OK)

        bill = Bill(calls)
        serializer = BillSerializer(bill)

        return Response(serializer.data)
