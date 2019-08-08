from django.conf.urls import include, url

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Call Records API",
      default_version='v1',
      description='Receives call detail records and calculates monthly bills for a given telephone number.',
      terms_of_service="https://opensource.org/licenses/BSD-3-Clause",
      contact=openapi.Contact(email="junio.webmaster@gmail.com"),
      license=openapi.License(name="New BSD License"),
   ),
   public=True,
)

urlpatterns = [
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/v1/calls/', include(('calls.urls', 'calls'))),
    url(r'^api/v1/bills/', include(('bills.urls', 'bills'))),
]
