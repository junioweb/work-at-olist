from rest_framework import viewsets

from .models import CallStart

from .serializers import CallStartSerializer


class CallStartViewSet(viewsets.ModelViewSet):
    queryset = CallStart.objects.all()
    serializer_class = CallStartSerializer
