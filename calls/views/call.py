import copy

from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response

from calls.domain.call import Call, CallEnd, CallStart
from calls.serializers import CallSerializer, CallEndSerializer, CallStartSerializer

from .base import BaseViewSet


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['started calls']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['started calls']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['started calls']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['started calls']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['started calls']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['started calls']))
class CallStartViewSet(BaseViewSet):
    queryset = CallStart.objects.all()
    serializer_class = CallStartSerializer
    filterset_fields = ('timestamp', 'source', 'destination', 'call_id')

    def create(self, request, *args, **kwargs):
        call, call_created = Call.objects.get_or_create(id=request.data['call_id'])

        try:
            return super().create(request, *args, **kwargs)
        except Exception as err:
            if call_created:
                call.delete()
            raise err


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['ended calls']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['ended calls']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['ended calls']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['ended calls']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['ended calls']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['ended calls']))
class CallEndViewSet(BaseViewSet):
    queryset = CallEnd.objects.all()
    serializer_class = CallEndSerializer
    filterset_fields = ('timestamp', 'call_id')

    def create(self, request, *args, **kwargs):
        call, call_created = Call.objects.get_or_create(id=request.data['call_id'])

        try:
            return super().create(request, *args, **kwargs)
        except Exception as err:
            if call_created:
                call.delete()
            raise err


class CallViewSet(BaseViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def create(self, request, *args, **kwargs):
        if Call.objects.filter(id=request.data['call_id']).exists():
            return redirect(reverse('calls:-detail', kwargs={'pk': request.data['call_id']}))

        call, call_created = Call.objects.get_or_create(id=request.data['call_id'])
        call_serializer = self.get_serializer(call)

        try:
            request_data = copy.deepcopy(request.data)
            if 'start' in request_data:
                request_data['start']['call_id'] = request_data['call_id']
                start_serializer = CallStartSerializer(data=request_data['start'])
                start_serializer.is_valid(raise_exception=True)
                start_serializer.save()
            if 'end' in request_data:
                request_data['end']['call_id'] = request_data['call_id']
                end_serializer = CallEndSerializer(data=request_data['end'])
                end_serializer.is_valid(raise_exception=True)
                end_serializer.save()

            headers = self.get_success_headers(call_serializer.data)
            return Response(call_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as err:
            if call_created:
                call.delete()
            raise err

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        call_instance = self.get_object()
        call_serializer = self.get_serializer(call_instance)

        request_data = copy.deepcopy(request.data)
        if 'start' in request_data:
            request_data['start']['call_id'] = call_instance.id
            start_instance = call_instance.start
            start_serializer = CallStartSerializer(start_instance, data=request_data['start'], partial=partial)
            start_serializer.is_valid(raise_exception=True)
            start_serializer.save()
        if 'end' in request_data:
            request_data['end']['call_id'] = call_instance.id
            end_instance = call_instance.end
            end_serializer = CallEndSerializer(end_instance, data=request_data['end'], partial=partial)
            end_serializer.is_valid(raise_exception=True)
            end_serializer.save()

        return Response(call_serializer.data)
