from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('', include('apps.quote.urls')),
    path('users/', include('apps.quote.urls')),
]
