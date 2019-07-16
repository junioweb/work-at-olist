from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/v1/calls/', include(('calls.urls', 'calls')))
]
