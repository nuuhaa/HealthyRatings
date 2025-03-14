from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # This remains unchanged
    path('tokenrequest/', obtain_auth_token)  # This remains unchanged
]