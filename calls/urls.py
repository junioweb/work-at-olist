from django.urls import include, path
from rest_framework import routers

from .views import CallStartViewSet, CallEndViewSet

router = routers.DefaultRouter()
router.register(r'start', CallStartViewSet, basename='start')
router.register(r'end', CallEndViewSet, basename='end')

urlpatterns = [
    path('', include(router.urls)),
]
