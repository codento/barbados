from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from . import routers


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(routers.router.urls, namespace='api')),
]
