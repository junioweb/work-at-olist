from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework import status, viewsets
from rest_framework.response import Response

from .exceptions import CallStartMissingError, TimestampLessThanCallStartTimestampError
from .exceptions import TimestampGreaterThanCallEndTimestampError, TypeCallMissingError

from .models import Call, CallEnd, CallStart

from .serializers import CallSerializer, CallEndSerializer, CallStartSerializer


class BaseViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except TypeCallMissingError as err:
            return Response({'detail': err.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return Response({}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CallStartViewSet(BaseViewSet):
    queryset = CallStart.objects.all()
    serializer_class = CallStartSerializer

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except TimestampGreaterThanCallEndTimestampError as err:
            return Response({'detail': err.message}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CallEndViewSet(BaseViewSet):
    queryset = CallEnd.objects.all()
    serializer_class = CallEndSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except CallStartMissingError as err:
            return Response({'detail': err.message}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except TimestampLessThanCallStartTimestampError as err:
            return Response({'detail': err.message}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


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
        except TypeCallMissingError as err:
            call.delete()
            return Response({'detail': err.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            call.delete()
            raise err

        headers = self.get_success_headers(call_serializer.data)
        return Response(call_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
