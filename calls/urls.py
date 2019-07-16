from django.urls import include, path
from rest_framework import routers

from .views import CallStartViewSet

router = routers.DefaultRouter()
router.register(r'start', CallStartViewSet, basename='start')

urlpatterns = [
    path('', include(router.urls)),
]
