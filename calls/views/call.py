from django.shortcuts import redirect
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response

from calls.exceptions import TypeCallMissingError
from calls.exceptions import RecordsMissingError, EmptyRecordsError
from calls.domain.call import Call, CallEnd, CallStart
from calls.serializers import CallSerializer, CallEndSerializer, CallStartSerializer

from .base import BaseViewSet


class CallStartViewSet(BaseViewSet):
    queryset = CallStart.objects.all()
    serializer_class = CallStartSerializer
    filterset_fields = ('timestamp', 'source', 'destination', 'call_id')


class CallEndViewSet(BaseViewSet):
    queryset = CallEnd.objects.all()
    serializer_class = CallEndSerializer
    filterset_fields = ('timestamp', 'call_id')


class CallViewSet(BaseViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def records_is_valid(self, request):
        if 'records' not in request.data:
            raise RecordsMissingError()
        if not len(request.data['records']):
            raise EmptyRecordsError()
        return True

    def type_record_is_valid(self, record):
        type_call = record.get('type')
        if type_call is None:
            raise TypeCallMissingError()
        return True

    def create(self, request, *args, **kwargs):
        if Call.objects.filter(id=request.data['call_id']).exists():
            return redirect(reverse('calls:-detail', kwargs={'pk': request.data['call_id']}))

        call_serializer = self.get_serializer(data=request.data)
        call_serializer.is_valid(raise_exception=True)
        call = call_serializer.save()

        try:
            self.records_is_valid(request)

            for record in request.data['records']:
                self.type_record_is_valid(record)
                type_call = record.get('type')
                record['call_id'] = call.id
                if type_call == 'start':
                    start_serializer = CallStartSerializer(data=record)
                    start_serializer.is_valid(raise_exception=True)
                    start_serializer.save()
                elif type_call == 'end':
                    end_serializer = CallEndSerializer(data=record)
                    end_serializer.is_valid(raise_exception=True)
                    end_serializer.save()
        except Exception as err:
            call.delete()
            raise err

        headers = self.get_success_headers(call_serializer.data)
        return Response(call_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        call_instance = self.get_object()
        start_serializer = None
        end_serializer = None

        self.records_is_valid(request)

        for record in request.data['records']:
            self.type_record_is_valid(record)
            type_call = record.get('type')
            record['call_id'] = call_instance.id
            if type_call == 'start':
                start_instance = call_instance.start
                start_serializer = CallStartSerializer(start_instance, data=record, partial=partial)
                start_serializer.is_valid(raise_exception=True)
            elif type_call == 'end':
                end_instance = call_instance.end
                end_serializer = CallEndSerializer(end_instance, data=record, partial=partial)
                end_serializer.is_valid(raise_exception=True)

        if start_serializer is not None:
            start_serializer.save()
        if end_serializer is not None:
            end_serializer.save()
        elif not partial:
            call_instance.end.delete()

        return super().update(request, *args, **kwargs)
