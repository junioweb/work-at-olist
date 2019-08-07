from django.urls import path

from .views import BillViewSet

urlpatterns = [
    path('', BillViewSet.as_view({'get': 'retrieve'}), name='bills'),
]
