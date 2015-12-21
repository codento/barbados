from django.contrib.auth import models as auth_models
from rest_framework.test import APIClient
import pytest
import json

from barbados.barbadosweb.test_fixtures import *


@pytest.fixture
def harbourmaster_user():
    user = tests.UserFactory.create()
    user.groups.add(auth_models.Group.objects.get(name__exact='Harbourmaster'))
    user.groups.add(auth_models.Group.objects.get(name__exact='Committee member'))
    user.groups.add(auth_models.Group.objects.get(name__exact='Member'))
    user.set_password('password')
    user.save()
    return user


@pytest.fixture
def secretary_user():
    user = tests.UserFactory.create()
    user.groups.add(auth_models.Group.objects.get(name__exact='Membership secretary'))
    user.groups.add(auth_models.Group.objects.get(name__exact='Committee member'))
    user.groups.add(auth_models.Group.objects.get(name__exact='Member'))
    user.set_password('password')
    user.save()
    return user


@pytest.fixture
def committee_member_user():
    user = tests.UserFactory.create()
    user.groups.add(auth_models.Group.objects.get(name__exact='Committee member'))
    user.groups.add(auth_models.Group.objects.get(name__exact='Member'))
    user.set_password('password')
    user.save()
    return user


@pytest.fixture
def other_ordinary_user():
    user = tests.UserFactory.create()
    user.groups.add(auth_models.Group.objects.get(name__exact='Member'))
    user.set_password('password')
    user.save()
    return user


# User tests

@pytest.mark.django_db()
def test_harbourmaster_list_users(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get('/api/user/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_get_other(harbourmaster_user, ordinary_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_list_users(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get('/api/user/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_get_other(secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_list_users(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get('/api/user/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_get_other(committee_member_user, ordinary_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_list_users(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/user/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_get_self(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_get_other(ordinary_user, other_ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/user/' + str(other_ordinary_user.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_user(ordinary_user):
    client = APIClient()

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_own_address(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    user_content['city'] = 'Atlantis'
    response = client.put('/api/user/' + str(ordinary_user.id) + '/', user_content, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_put_own_name(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    user_content['first_name'] = 'Ebeneezer'
    response = client.put('/api/user/' + str(ordinary_user.id) + '/', user_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_other_address(ordinary_user, other_ordinary_user):
    client = APIClient()
    assert client.login(username=other_ordinary_user.username, password='password')

    response = client.get('/api/user/' + str(other_ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    assert client.login(username=ordinary_user.username, password='password')

    user_content['city'] = 'Atlantis'
    response = client.put('/api/user/' + str(other_ordinary_user.id) + '/', user_content, format='json')
    assert response.status_code == 403

