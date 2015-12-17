from rest_framework import serializers
from barbados.barbadosdb import models


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:user-detail')

    boats = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='api:boat-detail', many=True)

    class Meta:
        model = models.User
        fields = (
            'first_name', 'last_name',
            'url', 'username', 'email',
            'birth_date', 'phone_number',
            'street_address', 'city', 'country_code',
            'boats'
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

    berth = serializers.HyperlinkedRelatedField(read_only=True, view_name='api:berth-detail')

    class Meta:
        model = models.Boat
        fields = ('url', 'user', 'name', 'berth',
                  'boat_type', 'model', 'manufacturer',
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

    harbours = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='api:harbour-detail', many=True)

    class Meta:
        model = models.Club
        fields = ('url', 'name', 'harbours')

    def create(self, validated_data):
        return models.Club.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class HarbourSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:harbour-detail')

    club = serializers.HyperlinkedRelatedField(queryset=models.Club.objects.all(), view_name='api:club-detail')
    jetties = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='api:jetty-detail', many=True)

    class Meta:
        model = models.Harbour
        fields = ('url', 'name', 'club', 'jetties')

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
    berths = serializers.HyperlinkedRelatedField(
        read_only=True, view_name='api:berth-detail', many=True)

    class Meta:
        model = models.Jetty
        fields = ('url', 'name', 'harbour', 'berths')

    def create(self, validated_data):
        return models.Jetty.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.harbour = validated_data.get('harbour', instance.harbour)
        instance.save()
        return instance


class BerthSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:berth-detail')

    boat = serializers.HyperlinkedRelatedField(
        queryset=models.Boat.objects.all(), view_name='api:boat-detail', allow_null=True, required=False)
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
