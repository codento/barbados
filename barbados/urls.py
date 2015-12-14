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

    def create(self, validated_data):
        return models.User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.street_address = validated_data.get('street_address', instance.street_address)
        instance.city = validated_data.get('city', instance.city)
        instance.country_code = validated_data.get('country_code', instance.country_code)
        instance.save()
        return instance


class BoatSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:boat-detail')
    user = serializers.HyperlinkedRelatedField(queryset=models.User.objects.all(), view_name='api:user-detail')

    class Meta:
        model = models.Boat
        fields = ('url', 'user', 'name', 'boat_type', 'model', 'manufacturer',
                  'registration_number', 'sail_number', 'boat_certificate_number',
                  'length', 'beam', 'height', 'draught', 'weight',
                  'material', 'colour',
                  'inspection_class', 'inspection_year', 'hull_inspection_year',
                  'insurance_company')

    def create(self, validated_data):
        return models.Boat.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.user = validated_data.get('user', instance.user)
        instance.boat_type = validated_data.get('boat_type', instance.boat_type)
        instance.model = validated_data.get('model', instance.model)
        instance.manufacturer = validated_data.get('manufacturer', instance.manufacturer)
        instance.registration_number = validated_data.get('registration_number', instance.registration_number)
        instance.sail_number = validated_data.get('sail_number', instance.sail_number)
        instance.boat_certificate_number = validated_data.get(
            'boat_certificate_number', instance.boat_certificate_number)
        instance.length = validated_data.get('length', instance.length)
        instance.beam = validated_data.get('beam', instance.beam)
        instance.height = validated_data.get('height', instance.height)
        instance.draught = validated_data.get('draught', instance.draught)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.material = validated_data.get('material', instance.material)
        instance.colour = validated_data.get('colour', instance.colour)
        instance.inspection_class = validated_data.get('inspection_class', instance.inspection_class)
        instance.inspection_year = validated_data.get('inspection_year', instance.inspection_year)
        instance.hull_inspection_year = validated_data.get('hull_inspection_year', instance.hull_inspection_year)
        instance.insurance_company = validated_data.get('insurance_company', instance.insurance_company)
        instance.save()
        return instance


class ClubSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:club-detail')

    class Meta:
        model = models.Club
        fields = ('url', 'name')

    def create(self, validated_data):
        return models.Club.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class HarbourSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:harbour-detail')

    club = serializers.HyperlinkedRelatedField(queryset=models.Club.objects.all(), view_name='api:club-detail')

    class Meta:
        model = models.Harbour
        fields = ('url', 'name', 'club')

    def create(self, validated_data):
        return models.Harbour.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.club = validated_data.get('club', instance.club)
        instance.save()
        return instance


class JettySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:jetty-detail')

    harbour = serializers.HyperlinkedRelatedField(queryset=models.Harbour.objects.all(), view_name='api:harbour-detail')

    class Meta:
        model = models.Jetty
        fields = ('url', 'name', 'harbour')

    def create(self, validated_data):
        return models.Jetty.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.harbour = validated_data.get('harbour', instance.harbour)
        instance.save()
        return instance


class BerthSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:berth-detail')

    boat = serializers.HyperlinkedRelatedField(queryset=models.Boat.objects.all(), view_name='api:boat-detail')
    jetty = serializers.HyperlinkedRelatedField(queryset=models.Jetty.objects.all(), view_name='api:jetty-detail')

    class Meta:
        model = models.Berth
        fields = ('url', 'boat', 'name', 'jetty')

    def create(self, validated_data):
        return models.Berth.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.jetty = validated_data.get('jetty', instance.jetty)
        instance.boat = validated_data.get('boat', instance.boat)
        instance.save()
        return instance


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer


class BoatViewSet(viewsets.ModelViewSet):
    queryset = models.Boat.objects.all()
    serializer_class = BoatSerializer


class ClubViewSet(viewsets.ModelViewSet):
    queryset = models.Club.objects.all()
    serializer_class = ClubSerializer


class HarbourViewSet(viewsets.ModelViewSet):
    queryset = models.Harbour.objects.all()
    serializer_class = HarbourSerializer


class JettyViewSet(viewsets.ModelViewSet):
    queryset = models.Jetty.objects.all()
    serializer_class = JettySerializer


class BerthViewSet(viewsets.ModelViewSet):
    queryset = models.Berth.objects.all()
    serializer_class = BerthSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'boat', BoatViewSet)
router.register(r'club', ClubViewSet)
router.register(r'harbour', HarbourViewSet)
router.register(r'jetty', JettyViewSet)
router.register(r'berth', BerthViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.STATIC_URL)

urlpatterns += [
    url(r'^api/', include(router.urls, namespace='api')),
]

