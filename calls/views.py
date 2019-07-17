from django.http import Http404

from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import CallStart

from .serializers import CallStartSerializer


class CallStartViewSet(viewsets.ModelViewSet):
    queryset = CallStart.objects.all()
    serializer_class = CallStartSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return Response({}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)
