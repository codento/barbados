from . import models

import pytest
import factory
from faker import Factory as FakerFactory
import random

faker = FakerFactory.create('fi_FI')

CLUB_SUFFIXES = [' Venekerho', ' Pursiseura', ' Veneseura']
HARBOUR_SUFFIXES = ['lahti', 'järvi', 'koski', 'nokka', 'niemi']


# Factories
class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    username = factory.LazyAttribute(lambda x: faker.user_name())
    password = factory.LazyAttribute(lambda x: faker.password())
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    phone_number = factory.LazyAttribute(lambda x: '+358' + str(100000000 + random.randint(0, 899999999)))


class BoatFactory(factory.Factory):
    class Meta:
        model = models.Boat

#    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda x: faker.first_name_female())
    registration_number = factory.Sequence(lambda n: chr((n % 26) + ord('A')) + str(10000 + n//26))


class ClubFactory(factory.Factory):
    class Meta:
        model = models.Club

    name = factory.Sequence(lambda n: faker.city_name() + CLUB_SUFFIXES[n % len(CLUB_SUFFIXES)])


class HarbourFactory(factory.Factory):
    class Meta:
        model = models.Harbour

#    club = factory.SubFactory(ClubFactory)
    name = factory.Sequence(lambda n: faker.fruit() + HARBOUR_SUFFIXES[n % len(HARBOUR_SUFFIXES)])


class JettyFactory(factory.Factory):
    class Meta:
        model = models.Jetty

#    harbour = factory.SubFactory(HarbourFactory)
    name = factory.sequence(lambda n: chr((n % 26) + ord('A')))


class BerthFactory(factory.Factory):
    class Meta:
        model = models.Berth

#    jetty = factory.SubFactory(JettyFactory)
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
    except models.ValidationError:
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
    c = ClubFactory.build()
    c.save()
    h = HarbourFactory.build(club=c)
    h.full_clean()
    h.save()


# Jetty

@pytest.mark.django_db()
def test_create_a_jetty():
    c = ClubFactory.build()
    c.save()
    h = HarbourFactory.build(club=c)
    h.save()
    j = JettyFactory.build(harbour=h)
    j.full_clean()
    j.save()


# Berth

@pytest.mark.django_db()
def test_create_a_berth():
    c = ClubFactory.build()
    c.save()
    h = HarbourFactory.build(club=c)
    h.save()
    j = JettyFactory.build(harbour=h)
    j.save()
    b = BerthFactory.build(jetty=j)
    b.full_clean()
    b.save()


# Boat

@pytest.mark.django_db()
def test_create_a_boat():
    u = UserFactory.build()
    u.save()
    b = BoatFactory.build(user=u)
    b.full_clean()
    b.save()


@pytest.mark.django_db()
def test_bad_boat_type():
    try:
        u = UserFactory.build()
        u.save()
        b = BoatFactory.build(user=u, boat_type='X')
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except models.ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_registration_number():
    try:
        u = UserFactory.build()
        u.save()
        b = BoatFactory.build(user=u, registration_number='hello')
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except models.ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_material():
    try:
        u = UserFactory.build()
        u.save()
        b = BoatFactory.build(user=u, material='X')
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except models.ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_inspection_class():
    try:
        u = UserFactory.build()
        u.save()
        b = BoatFactory.build(user=u, inspection_class=999)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except models.ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_inspection_year_too_short():
    try:
        u = UserFactory.build()
        u.save()
        b = BoatFactory.build(user=u, inspection_year=15)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except models.ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_inspection_year_in_future():
    try:
        u = UserFactory.build()
        u.save()
        b = BoatFactory.build(user=u, inspection_year=2030)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except models.ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_hull_inspection_year_too_short():
    try:
        u = UserFactory.build()
        u.save()
        b = BoatFactory.build(user=u, hull_inspection_year=15)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except models.ValidationError:
        pass


@pytest.mark.django_db()
def test_bad_hull_inspection_year_in_future():
    try:
        u = UserFactory.build()
        u.save()
        b = BoatFactory.build(user=u, hull_inspection_year=2030)
        b.full_clean()

        pytest.fail(msg='Boat should not be valid')
    except models.ValidationError:
        pass
