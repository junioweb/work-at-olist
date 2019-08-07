from rest_framework import viewsets, status
from rest_framework.response import Response

from calls.domain.call import Call, CallEnd
from bills.serializers import BillSerializer
from bills.exceptions import SubscriberNotPassedError


class BillViewSet(viewsets.ViewSet):
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

        queryset = Call.objects.prefetch_related('start', 'end')
        queryset = queryset.filter(start__source=subscriber, end__timestamp__month=month, end__timestamp__year=year)
        serializer = BillSerializer(queryset)

        if queryset.exists():
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_200_OK)
