from rest_framework.test import APIClient
import pytest
import json
import re
from django.core.urlresolvers import reverse

from barbados.barbadosdb import models
from barbados.barbadosweb.test_fixtures import *


def get_id(url):
    return re.findall('\/([0-9a-f\-]+)\/$', url)[0]


# User tests

@pytest.mark.django_db()
def test_get_users(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-list'))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 2   # don't forget admin user
    assert (content[0]['username'] == ordinary_user.username) or (content[1]['username'] == ordinary_user.username)


@pytest.mark.django_db()
def test_get_user(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['username'] == ordinary_user.username


@pytest.mark.django_db()
def test_create_user(admin_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.post(reverse('api:user-list'), {
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'secret',
        'city': 'Helsinki'
    }, format='json')
    assert response.status_code == 201
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['first_name'] == 'John'
    assert response['Location'] == content['url']

    id = get_id(content['url'])
    user = models.User.objects.get(pk=id)
    assert user.first_name == 'John'


@pytest.mark.django_db()
def test_modify_user_put(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    user_content['city'] = 'Tampere'
    response = client.put(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}), user_content, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['city'] == 'Tampere'

    ordinary_user.refresh_from_db()
    assert ordinary_user.city == 'Tampere'


@pytest.mark.django_db()
def test_modify_user_patch(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.patch(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}), {
        'city': 'Tampere'
    }, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['city'] == 'Tampere'

    ordinary_user.refresh_from_db()
    assert ordinary_user.city == 'Tampere'


@pytest.mark.django_db()
def test_delete_user(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.delete(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 204
    assert len(response.content) == 0

    assert not models.User.objects.filter(pk=ordinary_user.id).exists()


# Boat tests

@pytest.mark.django_db()
def test_get_boats(admin_user, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-list'))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == boat.name


@pytest.mark.django_db()
def test_get_boat(admin_user, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == boat.name


@pytest.mark.django_db()
def test_create_boat(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.post(reverse('api:boat-list'), {
        'user': user_url,
        'name': 'Titanic'
    }, format='json')
    assert response.status_code == 201
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Titanic'
    assert response['Location'] == content['url']

    id = get_id(content['url'])
    boat = models.Boat.objects.get(pk=id)
    assert boat.name == 'Titanic'


@pytest.mark.django_db()
def test_modify_boat_put(admin_user, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-list') + str(boat.id) + '/')
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']

    boat_content['name'] = 'Olympic'
    response = client.put(reverse('api:boat-list') + str(boat.id) + '/', boat_content, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Olympic'

    boat.refresh_from_db()
    assert boat.name == 'Olympic'


@pytest.mark.django_db()
def test_modify_boat_patch(admin_user, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.patch(reverse('api:boat-list') + str(boat.id) + '/', {
        'name': 'Olympic'
    }, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Olympic'

    boat.refresh_from_db()
    assert boat.name == 'Olympic'


@pytest.mark.django_db()
def test_delete_boat(admin_user, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.delete(reverse('api:boat-list') + str(boat.id) + '/')
    assert response.status_code == 204
    assert len(response.content) == 0

    assert not models.Boat.objects.filter(pk=boat.id).exists()


# Club tests

@pytest.mark.django_db()
def test_get_clubs(admin_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:club-list'))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == club.name


@pytest.mark.django_db()
def test_get_club(admin_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == club.name


@pytest.mark.django_db()
def test_create_club(admin_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.post(reverse('api:club-list'), {
        'name': 'Some Yacht Club'
    }, format='json')
    assert response.status_code == 201
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Some Yacht Club'
    assert response['Location'] == content['url']

    id = get_id(content['url'])
    club = models.Club.objects.get(pk=id)
    assert club.name == 'Some Yacht Club'


@pytest.mark.django_db()
def test_modify_club_put(admin_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    club_content = json.loads(response.content.decode('utf-8'))
    del club_content['url']
    del club_content['harbours']

    club_content['name'] = 'Other Yacht Club'
    response = client.put(reverse('api:club-detail', kwargs={'pk': club.id}), club_content, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Other Yacht Club'

    club.refresh_from_db()
    assert club.name == 'Other Yacht Club'


@pytest.mark.django_db()
def test_modify_club_patch(admin_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.patch(reverse('api:club-detail', kwargs={'pk': club.id}), {
        'name': 'Other Yacht Club'
    }, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Other Yacht Club'

    club.refresh_from_db()
    assert club.name == 'Other Yacht Club'


@pytest.mark.django_db()
def test_delete_club(admin_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.delete(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 204
    assert len(response.content) == 0

    assert not models.Club.objects.filter(pk=club.id).exists()


# Harbour tests

@pytest.mark.django_db()
def test_get_harbours(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-list'))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == harbour.name


@pytest.mark.django_db()
def test_get_harbour(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == harbour.name


@pytest.mark.django_db()
def test_create_harbour(admin_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    club_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.post(reverse('api:harbour-list'), {
        'club': club_url,
        'name': 'Some Harbour'
    }, format='json')
    assert response.status_code == 201
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Some Harbour'
    assert response['Location'] == content['url']

    id = get_id(content['url'])
    harbour = models.Harbour.objects.get(pk=id)
    assert harbour.name == 'Some Harbour'


@pytest.mark.django_db()
def test_modify_harbour_put(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_content = json.loads(response.content.decode('utf-8'))
    del harbour_content['url']
    del harbour_content['jetties']

    harbour_content['name'] = 'Other Harbour'
    response = client.put(reverse('api:harbour-detail', kwargs={'pk': harbour.id}), harbour_content, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Other Harbour'

    harbour.refresh_from_db()
    assert harbour.name == 'Other Harbour'


@pytest.mark.django_db()
def test_modify_harbour_patch(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.patch(reverse('api:harbour-detail', kwargs={'pk': harbour.id}), {
        'name': 'Other Harbour'
    }, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'Other Harbour'

    harbour.refresh_from_db()
    assert harbour.name == 'Other Harbour'


@pytest.mark.django_db()
def test_delete_harbour(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.delete(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 204
    assert len(response.content) == 0

    assert not models.Harbour.objects.filter(pk=harbour.id).exists()


# Jetty tests

@pytest.mark.django_db()
def test_get_jetties(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-list'))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == jetty.name


@pytest.mark.django_db()
def test_get_jetty(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == jetty.name


@pytest.mark.django_db()
def test_create_jetty(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.post(reverse('api:jetty-list'), {
        'harbour': harbour_url,
        'name': 'A'
    }, format='json')
    assert response.status_code == 201
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'A'
    assert response['Location'] == content['url']

    id = get_id(content['url'])
    jetty = models.Jetty.objects.get(pk=id)
    assert jetty.name == 'A'


@pytest.mark.django_db()
def test_modify_jetty_put(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_content = json.loads(response.content.decode('utf-8'))
    del jetty_content['url']
    del jetty_content['berths']

    jetty_content['name'] = 'ZZ'
    response = client.put(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), jetty_content, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'ZZ'

    jetty.refresh_from_db()
    assert jetty.name == 'ZZ'


@pytest.mark.django_db()
def test_modify_jetty_patch(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.patch(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), {
        'name': 'ZZ'
    }, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'ZZ'

    jetty.refresh_from_db()
    assert jetty.name == 'ZZ'


@pytest.mark.django_db()
def test_delete_jetty(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.delete(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 204
    assert len(response.content) == 0

    assert not models.Jetty.objects.filter(pk=jetty.id).exists()


# Berth tests

@pytest.mark.django_db()
def test_get_berths(admin_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-list'))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == berth.name


@pytest.mark.django_db()
def test_get_berth(admin_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == berth.name


@pytest.mark.django_db()
def test_create_berth(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.post(reverse('api:berth-list'), {
        'jetty': jetty_url,
        'name': '01'
    }, format='json')
    assert response.status_code == 201
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == '01'
    assert response['Location'] == content['url']

    id = get_id(content['url'])
    berth = models.Berth.objects.get(pk=id)
    assert berth.name == '01'


@pytest.mark.django_db()
def test_modify_berth_put(admin_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    berth_content['name'] = 'test'
    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'test'

    berth.refresh_from_db()
    assert berth.name == 'test'


@pytest.mark.django_db()
def test_modify_berth_patch(admin_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {
        'name': 'test'
    }, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['name'] == 'test'

    berth.refresh_from_db()
    assert berth.name == 'test'


@pytest.mark.django_db()
def test_delete_berth(admin_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')
    response = client.delete(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 204
    assert len(response.content) == 0

    assert not models.Berth.objects.filter(pk=berth.id).exists()


@pytest.mark.django_db()
def test_assign_berth_to_boat(admin_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-list') + str(boat.id) + '/')
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {
        'boat': boat_url
    }, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['boat'] == boat_url

    berth.refresh_from_db()
    assert berth.boat == boat


@pytest.mark.django_db()
def test_deny_berth_to_boat(admin_user, berth, boat):
    berth.boat = boat
    berth.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {
        'boat': None
    }, format='json')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert isinstance(content, dict)
    assert content['boat'] is None

    berth.refresh_from_db()
    assert berth.boat is None

