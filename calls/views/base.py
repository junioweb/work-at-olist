from django.http import Http404

from rest_framework import status, viewsets
from rest_framework.response import Response


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
