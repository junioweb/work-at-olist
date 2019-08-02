from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework import status, viewsets
from rest_framework.response import Response

from .exceptions import TypeCallMissingError
from .exceptions import RecordsMissingError, EmptyRecordsError

from .models import Call, CallEnd, CallStart

from .serializers import CallSerializer, CallEndSerializer, CallStartSerializer


class BaseViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
        except Http404:
            response = Response({}, status=status.HTTP_200_OK)

        return response

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
        except Http404:
            response = Response({}, status=status.HTTP_200_OK)

        return response


class CallStartViewSet(BaseViewSet):
    queryset = CallStart.objects.all()
    serializer_class = CallStartSerializer


class CallEndViewSet(BaseViewSet):
    queryset = CallEnd.objects.all()
    serializer_class = CallEndSerializer


class CallViewSet(BaseViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def create(self, request, *args, **kwargs):
        if Call.objects.filter(id=request.data['call_id']).exists():
            return redirect(reverse('calls:-detail', kwargs={'pk': request.data['call_id']}))

        call_serializer = self.get_serializer(data=request.data)
        call_serializer.is_valid(raise_exception=True)
        call = call_serializer.save()

        try:
            if 'records' not in request.data:
                raise RecordsMissingError()
            if not len(request.data['records']):
                raise EmptyRecordsError()

            for record in request.data['records']:
                type_call = record.get('type')
                if type_call is None:
                    raise TypeCallMissingError()

                record['call_id'] = call.id
                if type_call == 'start':
                    start_serializer = CallStartSerializer(data=record)
                    start_serializer.is_valid(raise_exception=True)
                    start_serializer.save()
                elif type_call == 'end':
                    end_serializer = CallEndSerializer(data=record)
                    end_serializer.is_valid(raise_exception=True)
                    end_serializer.save()
        finally:
            call.delete()

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        call_instance = self.get_object()
        start_serializer = None
        end_serializer = None

        if 'records' not in request.data:
            raise RecordsMissingError()
        if not len(request.data['records']):
            raise EmptyRecordsError()

        for record in request.data['records']:
            type_call = record.get('type')
            if type_call is None:
                raise TypeCallMissingError()

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
