from django.http import Http404

from rest_framework import status, viewsets
from rest_framework.response import Response

from .exceptions import CallStartMissingError, TimestampLessThanCallStartTimestampError

from .models import CallEnd, CallStart

from .serializers import CallEndSerializer, CallStartSerializer


class BaseViewSet(viewsets.ModelViewSet):
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
