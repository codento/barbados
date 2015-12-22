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
# GET

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
def test_unauthenticated_list_users():
    client = APIClient()

    response = client.get('/api/user/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_user(ordinary_user):
    client = APIClient()

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 403


# POST

@pytest.mark.django_db()
def test_harbourmaster_post_user(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.post('/api/user/', {
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'secret',
        'city': 'Helsinki'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_post_user(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.post('/api/user/', {
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'secret',
        'city': 'Helsinki'
    }, format='json')
    assert response.status_code == 201


@pytest.mark.django_db()
def test_committee_member_post_user(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.post('/api/user/', {
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'secret',
        'city': 'Helsinki'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_post_user(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.post('/api/user/', {
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'secret',
        'city': 'Helsinki'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_post_user():
    client = APIClient()

    response = client.post('/api/user/', {
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'secret',
        'city': 'Helsinki'
    }, format='json')
    assert response.status_code == 403


# PUT

@pytest.mark.django_db()
def test_ordinary_user_put_own_address(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    assert client.login(username=ordinary_user.username, password='password')

    user_content['city'] = 'Atlantis'
    response = client.put('/api/user/' + str(ordinary_user.id) + '/', user_content, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_put_own_name(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    assert client.login(username=ordinary_user.username, password='password')

    user_content['first_name'] = 'Ebeneezer'
    response = client.put('/api/user/' + str(ordinary_user.id) + '/', user_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_other_address(admin_user, ordinary_user, other_ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/user/' + str(other_ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    assert client.login(username=ordinary_user.username, password='password')

    user_content['city'] = 'Atlantis'
    response = client.put('/api/user/' + str(other_ordinary_user.id) + '/', user_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_put_other_address(admin_user, secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    assert client.login(username=secretary_user.username, password='password')

    user_content['city'] = 'Atlantis'
    response = client.put('/api/user/' + str(ordinary_user.id) + '/', user_content, format='json')
    assert response.status_code == 200


# PATCH

@pytest.mark.django_db()
def test_ordinary_user_patch_own_address(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch('/api/user/' + str(ordinary_user.id) + '/', {'city': 'Atlantis'}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_patch_own_name(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch('/api/user/' + str(ordinary_user.id) + '/', {'first_name': 'Ebeneezer'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_other_address(ordinary_user, other_ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch('/api/user/' + str(other_ordinary_user.id) + '/', {'city': 'Atlantis'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_patch_other_address(secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.patch('/api/user/' + str(ordinary_user.id) + '/', {'city': 'Atlantis'}, format='json')
    assert response.status_code == 200


# DELETE

@pytest.mark.django_db()
def test_secretary_delete_user(secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.delete('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 204


@pytest.mark.django_db()
def test_harbourmaster_delete_user(harbourmaster_user, ordinary_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.delete('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_delete_user(committee_member_user, ordinary_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.delete('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_delete_other(ordinary_user, other_ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.delete('/api/user/' + str(other_ordinary_user.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_delete_user(ordinary_user):
    client = APIClient()

    response = client.delete('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 403

# We have no special treatment for secretary or ordinary user deleting themselves


# Boat tests
# GET

@pytest.mark.django_db()
def test_harbourmaster_list_boats(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get('/api/boat/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_get_other_boat(harbourmaster_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_list_boats(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get('/api/boat/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_get_other_boat(secretary_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_list_boats(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get('/api/boat/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_get_other_boat(committee_member_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_list_boats(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/boat/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_get_own_boat(ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_get_other_boat(ordinary_user, other_ordinary_user, boat):
    boat.user = other_ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_list_boats():
    client = APIClient()

    response = client.get('/api/boat/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_boat(boat):
    client = APIClient()

    response = client.get('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 403


# POST

@pytest.mark.django_db()
def test_harbourmaster_post_boat(admin_user, harbourmaster_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    user_url = user_content['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.post('/api/boat/', {
        'user': user_url,
        'name': 'African Queen'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_post_boat(admin_user, secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    user_url = user_content['url']

    assert client.login(username=secretary_user.username, password='password')

    response = client.post('/api/boat/', {
        'user': user_url,
        'name': 'African Queen'
    }, format='json')
    assert response.status_code == 201


@pytest.mark.django_db()
def test_committee_member_post_boat(admin_user, committee_member_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    user_url = user_content['url']

    assert client.login(username=committee_member_user.username, password='password')

    response = client.post('/api/boat/', {
        'user': user_url,
        'name': 'African Queen'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_post_boat(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    user_url = user_content['url']

    assert client.login(username=ordinary_user.username, password='password')

    response = client.post('/api/boat/', {
        'user': user_url,
        'name': 'African Queen'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_post_boat(admin_user, ordinary_user):
    client = APIClient()

    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/user/' + str(ordinary_user.id) + '/')
    user_content = json.loads(response.content.decode('utf-8'))
    user_url = user_content['url']

    client.logout()

    response = client.post('/api/boat/', {
        'user': user_url,
        'name': 'African Queen'
    }, format='json')
    assert response.status_code == 403


# PUT

@pytest.mark.django_db()
def test_ordinary_user_put_own_boat_name(admin_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/boat/' + str(boat.id) + '/')
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    assert client.login(username=ordinary_user.username, password='password')

    boat_content['name'] = 'African Queen'
    response = client.put('/api/boat/' + str(boat.id) + '/', boat_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_own_boat_berth(admin_user, ordinary_user, boat, berth):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/boat/' + str(boat.id) + '/')
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    response = client.get('/api/berth/' + str(berth.id) + '/')
    berth_content = json.loads(response.content.decode('utf-8'))
    berth_url = berth_content['url']

    assert client.login(username=ordinary_user.username, password='password')

    boat_content['berth'] = berth_url
    response = client.put('/api/boat/' + str(boat.id) + '/', boat_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_other_boat_name(admin_user, ordinary_user, other_ordinary_user, boat):
    boat.user = other_ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/boat/' + str(boat.id) + '/')
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    assert client.login(username=ordinary_user.username, password='password')

    boat_content['city'] = 'Atlantis'
    response = client.put('/api/boat/' + str(boat.id) + '/', boat_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_put_other_boat_name(admin_user, secretary_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/boat/' + str(boat.id) + '/')
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    assert client.login(username=secretary_user.username, password='password')

    boat_content['name'] = 'African Queen'
    response = client.put('/api/boat/' + str(boat.id) + '/', boat_content, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_put_boat_berth(admin_user, harbourmaster_user, ordinary_user, boat, berth):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/boat/' + str(boat.id) + '/')
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    response = client.get('/api/berth/' + str(berth.id) + '/')
    berth_content = json.loads(response.content.decode('utf-8'))
    berth_url = berth_content['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    boat_content['berth'] = berth_url
    response = client.put('/api/boat/' + str(boat.id) + '/', boat_content, format='json')
    assert response.status_code == 200


# PATCH

@pytest.mark.django_db()
def test_ordinary_user_patch_own_boat_name(ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch('/api/boat/' + str(boat.id) + '/', {'name': 'African Queen'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_own_boat_berth(admin_user, ordinary_user, boat, berth):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/berth/' + str(berth.id) + '/')
    berth_content = json.loads(response.content.decode('utf-8'))
    berth_url = berth_content['url']

    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch('/api/boat/' + str(boat.id) + '/', {'berth': berth_url}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_other_boat_name(ordinary_user, other_ordinary_user, boat):
    boat.user = other_ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch('/api/boat/' + str(boat.id) + '/', {'name': 'African Queen'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_patch_other_boat_name(secretary_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.patch('/api/boat/' + str(boat.id) + '/', {'name': 'African Queen'}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_patch_boat_berth(admin_user, harbourmaster_user, ordinary_user, boat, berth):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get('/api/berth/' + str(berth.id) + '/')
    berth_content = json.loads(response.content.decode('utf-8'))
    berth_url = berth_content['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.patch('/api/boat/' + str(boat.id) + '/', {'berth': berth_url}, format='json')
    assert response.status_code == 200


# DELETE

@pytest.mark.django_db()
def test_secretary_delete_boat(secretary_user, boat):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.delete('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 204


@pytest.mark.django_db()
def test_harbourmaster_delete_boat(harbourmaster_user, boat):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.delete('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_delete_boat(committee_member_user, boat):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.delete('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_delete_boat(ordinary_user, boat):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.delete('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_delete_boat(boat):
    client = APIClient()

    response = client.delete('/api/boat/' + str(boat.id) + '/')
    assert response.status_code == 403


# Club tests
# GET

@pytest.mark.django_db()
def test_harbourmaster_list_clubs(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get('/api/club/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_get_club(harbourmaster_user, club):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get('/api/club/' + str(club.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_list_clubs(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get('/api/club/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_get_club(secretary_user, club):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get('/api/club/' + str(club.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_list_clubs(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get('/api/club/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_get_club(committee_member_user, club):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get('/api/club/' + str(club.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_list_clubs(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/club/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_get_club(ordinary_user, club):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get('/api/club/' + str(club.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_unauthenticated_list_clubs():
    client = APIClient()

    response = client.get('/api/club/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_club(club):
    client = APIClient()

    response = client.get('/api/club/' + str(club.id) + '/')
    assert response.status_code == 403


# POST

@pytest.mark.django_db()
def test_harbourmaster_post_club(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.post('/api/club/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_post_club(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.post('/api/club/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_post_club(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.post('/api/club/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_post_club(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.post('/api/club/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_post_club():
    client = APIClient()

    response = client.post('/api/club/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


# PUT

@pytest.mark.django_db()
def test_harbourmaster_put_club(harbourmaster_user, club):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.put('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_put_club(secretary_user, club):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.put('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_put_club(committee_member_user, club):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.put('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_club(ordinary_user, club):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.put('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_put_club(club):
    client = APIClient()

    response = client.put('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


# PATCH

@pytest.mark.django_db()
def test_harbourmaster_patch_club(harbourmaster_user, club):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.patch('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_patch_club(secretary_user, club):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.patch('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_patch_club(committee_member_user, club):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.patch('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_club(ordinary_user, club):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_patch_club(club):
    client = APIClient()

    response = client.patch('/api/club/' + str(club.id) + '/', {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


# DELETE

@pytest.mark.django_db()
def test_secretary_delete_club(secretary_user, club):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.delete('/api/club/' + str(club.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_harbourmaster_delete_club(harbourmaster_user, club):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.delete('/api/club/' + str(club.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_delete_club(committee_member_user, club):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.delete('/api/club/' + str(club.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_delete_club(ordinary_user, club):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.delete('/api/club/' + str(club.id) + '/')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_delete_club(club):
    client = APIClient()

    response = client.delete('/api/club/' + str(club.id) + '/')
    assert response.status_code == 403

