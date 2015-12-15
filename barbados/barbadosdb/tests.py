from django.contrib.auth import models as auth_models
from django.core.exceptions import ValidationError
from . import models

import pytest
import factory
from faker import Factory as FakerFactory
import random

faker = FakerFactory.create('fi_FI')

CLUB_SUFFIXES = [' Venekerho', ' Pursiseura', ' Veneseura']
HARBOUR_SUFFIXES = ['lahti', 'järvi', 'koski', 'nokka', 'niemi']


# Factories
class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.LazyAttribute(lambda x: faker.user_name())
    password = factory.LazyAttribute(lambda x: faker.password())
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    phone_number = factory.LazyAttribute(lambda x: '+358' + str(100000000 + random.randint(0, 899999999)))


class BoatFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Boat

    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda x: faker.first_name_female())
    registration_number = factory.Sequence(lambda n: chr((n % 26) + ord('A')) + str(10000 + n // 26))


class ClubFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Club

    name = factory.Sequence(lambda n: faker.city_name() + CLUB_SUFFIXES[n % len(CLUB_SUFFIXES)])


class HarbourFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Harbour

    club = factory.SubFactory(ClubFactory)
    name = factory.Sequence(lambda n: faker.fruit() + HARBOUR_SUFFIXES[n % len(HARBOUR_SUFFIXES)])


class JettyFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Jetty

    harbour = factory.SubFactory(HarbourFactory)
    name = factory.sequence(lambda n: chr((n % 26) + ord('A')))


class BerthFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Berth

    jetty = factory.SubFactory(JettyFactory)
    name = factory.Sequence(lambda n: str(n))


# User

@pytest.mark.django_db()
def test_create_a_user():
    u = UserFactory.build()
    u.full_clean()
    u.save()


@pytest.mark.django_db()
def test_bad_phone_number():
    try:
        u = UserFactory.build(phone_number='123')
        u.full_clean()

        pytest.fail(msg='User should not be valid')
    except ValidationError:
        pass


# Club

@pytest.mark.django_db()
def test_create_a_club():
    c = ClubFactory.build()
    c.full_clean()
    c.save()


# Harbour

@pytest.mark.django_db()
def test_create_a_harbour():
    h = HarbourFactory.build()
    h.club.save()
    h.full_clean()
    h.save()


# Jetty

@pytest.mark.django_db()
def test_create_a_jetty():
    j = JettyFactory.build()
    j.harbour.save()
    j.full_clean()
    j.save()


# Berth

@pytest.mark.django_db()
def test_create_a_berth():
    b = BerthFactory.build()
    b.jetty.save()
    b.full_clean()
    b.save()


# Boat

@pytest.mark.django_db()
def test_create_a_boat():
    b = BoatFactory.build()
    b.user.save()
    b.full_clean()
    b.save()


@pytest.mark.django_db()
def test_bad_boat_type():
    try:
        b = BoatFactory.build(boat_type='X')
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_registration_number():
    try:
        b = BoatFactory.build(registration_number='hello')
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_material():
    try:
        b = BoatFactory.build(material='X')
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_inspection_class():
    try:
        b = BoatFactory.build(inspection_class=999)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_inspection_year_too_short():
    try:
        b = BoatFactory.build(inspection_year=15)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_inspection_year_in_future():
    try:
        b = BoatFactory.build(inspection_year=2030)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_hull_inspection_year_too_short():
    try:
        b = BoatFactory.build(hull_inspection_year=15)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_hull_inspection_year_in_future():
    try:
        b = BoatFactory.build(hull_inspection_year=2030)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except ValidationError:
        pass


@pytest.mark.django_db()
def test_assign_boat_to_berth():
    boat = BoatFactory.create()
    berth = BerthFactory.create()
    berth.boat = boat
    berth.save()
    boat.refresh_from_db()
    assert boat.berth == berth


@pytest.mark.django_db()
def test_secretary_permissions():
    u = UserFactory.create()
    g = auth_models.Group.objects.get(name='Membership secretary')

    u.groups.add(g)

    assert u.has_perm('barbadosdb.add_boat')
    assert u.has_perm('barbadosdb.add_user')
    assert not u.has_perm('barbadosdb.assign_berth_boat')


@pytest.mark.django_db()
def test_user_berth_permission():
    u = UserFactory.create()
    group = auth_models.Group.objects.get(name='Harbourmaster')

    u.groups.add(group)

    assert u.has_perm('barbadosdb.assign_berth_boat')
    assert not u.has_perm('barbadosdb.add_user')
    assert not u.has_perm('barbadosdb.add_boat')

