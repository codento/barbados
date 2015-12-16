from django.contrib.auth import models as auth_models
from rest_framework.test import APIClient
import pytest
import json

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


# User tests


@pytest.mark.django_db()
def test_get_users(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/user/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 2   # don't forget admin user
    assert (content[0]['username'] == ordinary_user.username) or (content[1]['username'] == ordinary_user.username)


@pytest.mark.django_db()
def test_get_user(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['username'] == ordinary_user.username


# Boat tests

@pytest.mark.django_db()
def test_get_boats(admin_user, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/boat/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == boat.name


@pytest.mark.django_db()
def test_get_boat(admin_user, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == boat.name


@pytest.mark.django_db()
def test_create_boat(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_url = json.loads(response.content.decode('utf-8'))['url']
    response = client.post('/api/boat/', {
        'user': user_url,
        'name': 'Titanic'
    }, format='json')
    assert response.status_code == 201
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Titanic'


# Club tests

@pytest.mark.django_db()
def test_get_clubs(admin_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/club/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == club.name


@pytest.mark.django_db()
def test_get_club(admin_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/club/' + str(club.id) + '/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == club.name


# Harbour tests

@pytest.mark.django_db()
def test_get_harbours(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/harbour/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == harbour.name


@pytest.mark.django_db()
def test_get_harbour(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/harbour/' + str(harbour.id) + '/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == harbour.name


# Jetty tests


@pytest.mark.django_db()
def test_get_jetties(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/jetty/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == jetty.name


@pytest.mark.django_db()
def test_get_jetty(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/jetty/' + str(jetty.id) + '/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == jetty.name


# Berth tests

@pytest.mark.django_db()
def test_get_berths(admin_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/berth/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == berth.name


@pytest.mark.django_db()
def test_get_berth(admin_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.get('/api/berth/' + str(berth.id) + '/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == berth.name

