"""barbados URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from barbados.barbadosdb import models

from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'url', 'username', 'email',
            'birth_date', 'phone_number',
            'street_address', 'city', 'country_code'
        )


class ClubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Club
        fields = ('name')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.STATIC_URL)

