from django.contrib.auth import models as auth_models
import pytest

from barbados.barbadosdb import tests


@pytest.fixture
def admin_user():
    user = tests.UserFactory.create()
    user.is_superuser = True
    user.set_password('password')
    user.save()
    return user


@pytest.fixture
def harbourmaster_user():
    user = tests.UserFactory.create()
    user.groups.add(auth_models.Group.objects.get(name__exact='Harbourmaster'))
    user.set_password('password')
    user.save()
    return user


@pytest.fixture
def secretary_user():
    user = tests.UserFactory.create()
    user.groups.add(auth_models.Group.objects.get(name__exact='Membership secretary'))
    user.set_password('password')
    user.save()
    return user


@pytest.fixture
def committee_member_user():
    user = tests.UserFactory.create()
    user.groups.add(auth_models.Group.objects.get(name__exact='Committee member'))
    user.set_password('password')
    user.save()
    return user


@pytest.fixture
def ordinary_user():
    user = tests.UserFactory.create()
    user.set_password('password')
    user.save()
    return user


@pytest.fixture
def boat():
    return tests.BoatFactory.create()


@pytest.fixture
def club():
    return tests.ClubFactory.create()


@pytest.fixture
def harbour():
    return tests.HarbourFactory.create()


@pytest.fixture
def jetty():
    return tests.JettyFactory.create()


@pytest.fixture
def berth():
    return tests.BerthFactory.create()

