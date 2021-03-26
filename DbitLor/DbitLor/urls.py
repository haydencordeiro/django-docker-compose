from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

urlpatterns = [
    path('', include('endpointApp.urls')),
    path('admin/', admin.site.urls),
    path('api/password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('api-auth/', include('rest_framework.urls'))
    # url(r'^auth/', include('djoser.urls')),
]
