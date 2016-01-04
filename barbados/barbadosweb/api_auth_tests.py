from django.contrib.auth import models as auth_models
from rest_framework.test import APIClient
import pytest
import json
from django.core.urlresolvers import reverse

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

    response = client.get(reverse('api:user-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_get_other(harbourmaster_user, ordinary_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_list_users(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:user-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_get_other(secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_list_users(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:user-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_get_other(committee_member_user, ordinary_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_list_users(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:user-list'))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_get_self(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_get_other(ordinary_user, other_ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': other_ordinary_user.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_list_users():
    client = APIClient()

    response = client.get(reverse('api:user-list'))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_user(ordinary_user):
    client = APIClient()

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 403


# POST

@pytest.mark.django_db()
def test_harbourmaster_post_user(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.post(reverse('api:user-list'), {
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

    response = client.post(reverse('api:user-list'), {
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

    response = client.post(reverse('api:user-list'), {
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

    response = client.post(reverse('api:user-list'), {
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

    response = client.post(reverse('api:user-list'), {
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

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    assert client.login(username=ordinary_user.username, password='password')

    user_content['city'] = 'Atlantis'
    response = client.put(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}), user_content, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_put_own_name(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    assert client.login(username=ordinary_user.username, password='password')

    user_content['first_name'] = 'Ebeneezer'
    response = client.put(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}), user_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_other_address(admin_user, ordinary_user, other_ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': other_ordinary_user.id}))
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    assert client.login(username=ordinary_user.username, password='password')

    user_content['city'] = 'Atlantis'
    response = client.put(
        reverse('api:user-detail', kwargs={'pk': other_ordinary_user.id}), user_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_put_other_address(admin_user, secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_content = json.loads(response.content.decode('utf-8'))
    del user_content['url']
    del user_content['boats']

    assert client.login(username=secretary_user.username, password='password')

    user_content['city'] = 'Atlantis'
    response = client.put(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}), user_content, format='json')
    assert response.status_code == 200


# PATCH

@pytest.mark.django_db()
def test_ordinary_user_patch_own_address(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(
        reverse('api:user-detail', kwargs={'pk': ordinary_user.id}), {'city': 'Atlantis'}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_patch_own_name(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(
        reverse('api:user-detail', kwargs={'pk': ordinary_user.id}), {'first_name': 'Ebeneezer'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_other_address(ordinary_user, other_ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(
        reverse('api:user-detail', kwargs={'pk': other_ordinary_user.id}), {'city': 'Atlantis'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_patch_other_address(secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.patch(
        reverse('api:user-detail', kwargs={'pk': ordinary_user.id}), {'city': 'Atlantis'}, format='json')
    assert response.status_code == 200


# DELETE

@pytest.mark.django_db()
def test_secretary_delete_user(secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.delete(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 204


@pytest.mark.django_db()
def test_harbourmaster_delete_user(harbourmaster_user, ordinary_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.delete(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_delete_user(committee_member_user, ordinary_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.delete(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_delete_other(ordinary_user, other_ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.delete(reverse('api:user-detail', kwargs={'pk': other_ordinary_user.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_delete_user(ordinary_user):
    client = APIClient()

    response = client.delete(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 403

# We have no special treatment for secretary or ordinary user deleting themselves


# Boat tests
# GET

@pytest.mark.django_db()
def test_harbourmaster_list_boats(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:boat-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_get_other_boat(harbourmaster_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_list_boats(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:boat-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_get_other_boat(secretary_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_list_boats(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:boat-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_get_other_boat(committee_member_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_list_boats(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:boat-list'))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_get_own_boat(ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_get_other_boat(ordinary_user, other_ordinary_user, boat):
    boat.user = other_ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_list_boats():
    client = APIClient()

    response = client.get(reverse('api:boat-list'))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_boat(boat):
    client = APIClient()

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 403


# POST

@pytest.mark.django_db()
def test_harbourmaster_post_boat(admin_user, harbourmaster_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.post(reverse('api:boat-list'), {
        'user': user_url,
        'name': 'African Queen'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_post_boat(admin_user, secretary_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=secretary_user.username, password='password')

    response = client.post(reverse('api:boat-list'), {
        'user': user_url,
        'name': 'African Queen'
    }, format='json')
    assert response.status_code == 201


@pytest.mark.django_db()
def test_committee_member_post_boat(admin_user, committee_member_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=committee_member_user.username, password='password')

    response = client.post(reverse('api:boat-list'), {
        'user': user_url,
        'name': 'African Queen'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_post_boat(admin_user, ordinary_user):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=ordinary_user.username, password='password')

    response = client.post(reverse('api:boat-list'), {
        'user': user_url,
        'name': 'African Queen'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_post_boat(admin_user, ordinary_user):
    client = APIClient()

    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:user-detail', kwargs={'pk': ordinary_user.id}))
    user_url = json.loads(response.content.decode('utf-8'))['url']

    client.logout()

    response = client.post(reverse('api:boat-list'), {
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

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    assert client.login(username=ordinary_user.username, password='password')

    boat_content['name'] = 'African Queen'
    response = client.put(reverse('api:boat-detail', kwargs={'pk': boat.id}), boat_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_own_boat_berth(admin_user, ordinary_user, boat, berth):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=ordinary_user.username, password='password')

    boat_content['berth'] = berth_url
    response = client.put(reverse('api:boat-detail', kwargs={'pk': boat.id}), boat_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_other_boat_name(admin_user, ordinary_user, other_ordinary_user, boat):
    boat.user = other_ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    assert client.login(username=ordinary_user.username, password='password')

    boat_content['city'] = 'Atlantis'
    response = client.put(reverse('api:boat-detail', kwargs={'pk': boat.id}), boat_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_put_other_boat_name(admin_user, secretary_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    assert client.login(username=secretary_user.username, password='password')

    boat_content['name'] = 'African Queen'
    response = client.put(reverse('api:boat-detail', kwargs={'pk': boat.id}), boat_content, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_put_boat_berth(admin_user, harbourmaster_user, ordinary_user, boat, berth):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_content = json.loads(response.content.decode('utf-8'))
    del boat_content['url']
    del boat_content['berth']

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    boat_content['berth'] = berth_url
    response = client.put(reverse('api:boat-detail', kwargs={'pk': boat.id}), boat_content, format='json')
    assert response.status_code == 200


# PATCH

@pytest.mark.django_db()
def test_ordinary_user_patch_own_boat_name(ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(
        reverse('api:boat-detail', kwargs={'pk': boat.id}), {'name': 'African Queen'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_own_boat_berth(admin_user, ordinary_user, boat, berth):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(reverse('api:boat-detail', kwargs={'pk': boat.id}), {'berth': berth_url}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_other_boat_name(ordinary_user, other_ordinary_user, boat):
    boat.user = other_ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(
        reverse('api:boat-detail', kwargs={'pk': boat.id}), {'name': 'African Queen'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_patch_other_boat_name(secretary_user, ordinary_user, boat):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.patch(
        reverse('api:boat-detail', kwargs={'pk': boat.id}), {'name': 'African Queen'}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_patch_boat_berth(admin_user, harbourmaster_user, ordinary_user, boat, berth):
    boat.user = ordinary_user
    boat.save()

    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.patch(reverse('api:boat-detail', kwargs={'pk': boat.id}), {'berth': berth_url}, format='json')
    assert response.status_code == 200


# DELETE

@pytest.mark.django_db()
def test_secretary_delete_boat(secretary_user, boat):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.delete(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 204


@pytest.mark.django_db()
def test_harbourmaster_delete_boat(harbourmaster_user, boat):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.delete(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_delete_boat(committee_member_user, boat):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.delete(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_delete_boat(ordinary_user, boat):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.delete(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_delete_boat(boat):
    client = APIClient()

    response = client.delete(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    assert response.status_code == 403


# Club tests
# GET

@pytest.mark.django_db()
def test_harbourmaster_list_clubs(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:club-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_get_club(harbourmaster_user, club):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_list_clubs(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:club-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_get_club(secretary_user, club):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_list_clubs(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:club-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_get_club(committee_member_user, club):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_list_clubs(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:club-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_get_club(ordinary_user, club):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_unauthenticated_list_clubs():
    client = APIClient()

    response = client.get(reverse('api:club-list'))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_club(club):
    client = APIClient()

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 403


# POST

@pytest.mark.django_db()
def test_harbourmaster_post_club(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.post(reverse('api:club-list'), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_post_club(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.post(reverse('api:club-list'), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_post_club(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.post(reverse('api:club-list'), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_post_club(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.post(reverse('api:club-list'), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_post_club():
    client = APIClient()

    response = client.post(reverse('api:club-list'), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


# PUT

@pytest.mark.django_db()
def test_harbourmaster_put_club(harbourmaster_user, club):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.put(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_put_club(secretary_user, club):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.put(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_put_club(committee_member_user, club):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.put(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_club(ordinary_user, club):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.put(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_put_club(club):
    client = APIClient()

    response = client.put(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


# PATCH

@pytest.mark.django_db()
def test_harbourmaster_patch_club(harbourmaster_user, club):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.patch(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_patch_club(secretary_user, club):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.patch(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_patch_club(committee_member_user, club):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.patch(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_club(ordinary_user, club):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_patch_club(club):
    client = APIClient()

    response = client.patch(reverse('api:club-detail', kwargs={'pk': club.id}), {'name': 'Some Club'}, format='json')
    assert response.status_code == 403


# DELETE

@pytest.mark.django_db()
def test_secretary_delete_club(secretary_user, club):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.delete(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_harbourmaster_delete_club(harbourmaster_user, club):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.delete(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_delete_club(committee_member_user, club):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.delete(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_delete_club(ordinary_user, club):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.delete(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_delete_club(club):
    client = APIClient()

    response = client.delete(reverse('api:club-detail', kwargs={'pk': club.id}))
    assert response.status_code == 403


# Harbour tests
# GET

@pytest.mark.django_db()
def test_harbourmaster_list_harbours(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:harbour-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_get_harbour(harbourmaster_user, harbour):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_list_harbours(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:harbour-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_get_harbour(secretary_user, harbour):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_list_harbours(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:harbour-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_get_harbour(committee_member_user, harbour):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_list_harbours(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:harbour-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_get_harbour(ordinary_user, harbour):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_unauthenticated_list_harbours():
    client = APIClient()

    response = client.get(reverse('api:harbour-list'))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_harbour(harbour):
    client = APIClient()

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 403


# POST

@pytest.mark.django_db()
def test_harbourmaster_post_harbour(admin_user, harbourmaster_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    club_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.post(reverse('api:harbour-list'), {
        'club': club_url,
        'name': 'Kalasatama'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_post_harbour(admin_user, secretary_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    club_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=secretary_user.username, password='password')

    response = client.post(reverse('api:harbour-list'), {
        'club': club_url,
        'name': 'Kalasatama'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_post_harbour(admin_user, committee_member_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    club_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=committee_member_user.username, password='password')

    response = client.post(reverse('api:harbour-list'), {
        'club': club_url,
        'name': 'Kalasatama'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_post_harbour(admin_user, ordinary_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    club_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=ordinary_user.username, password='password')

    response = client.post(reverse('api:harbour-list'), {
        'club': club_url,
        'name': 'Kalasatama'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_post_harbour(admin_user, club):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:club-detail', kwargs={'pk': club.id}))
    club_url = json.loads(response.content.decode('utf-8'))['url']

    client.logout()

    response = client.post(reverse('api:harbour-list'), {
        'club': club_url,
        'name': 'Kalasatama'
    }, format='json')
    assert response.status_code == 403


# PUT

@pytest.mark.django_db()
def test_harbourmaster_put_harbour(admin_user, harbourmaster_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_content = json.loads(response.content.decode('utf-8'))
    del harbour_content['url']
    del harbour_content['jetties']

    assert client.login(username=harbourmaster_user.username, password='password')

    harbour_content['name'] = 'Kalasatama'
    response = client.put(reverse('api:harbour-detail', kwargs={'pk': harbour.id}), harbour_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_put_harbour(admin_user, secretary_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_content = json.loads(response.content.decode('utf-8'))
    del harbour_content['url']
    del harbour_content['jetties']

    assert client.login(username=secretary_user.username, password='password')

    harbour_content['name'] = 'Kalasatama'
    response = client.put(reverse('api:harbour-detail', kwargs={'pk': harbour.id}), harbour_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_put_harbour(admin_user, committee_member_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_content = json.loads(response.content.decode('utf-8'))
    del harbour_content['url']
    del harbour_content['jetties']

    assert client.login(username=committee_member_user.username, password='password')

    harbour_content['name'] = 'Kalasatama'
    response = client.put(reverse('api:harbour-detail', kwargs={'pk': harbour.id}), harbour_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_harbour(admin_user, ordinary_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_content = json.loads(response.content.decode('utf-8'))
    del harbour_content['url']
    del harbour_content['jetties']

    assert client.login(username=ordinary_user.username, password='password')

    harbour_content['name'] = 'Kalasatama'
    response = client.put(reverse('api:harbour-detail', kwargs={'pk': harbour.id}), harbour_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_put_harbour(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_content = json.loads(response.content.decode('utf-8'))
    del harbour_content['url']
    del harbour_content['jetties']

    client.logout()

    harbour_content['name'] = 'Kalasatama'
    response = client.put(reverse('api:harbour-detail', kwargs={'pk': harbour.id}), harbour_content, format='json')
    assert response.status_code == 403


# PATCH

@pytest.mark.django_db()
def test_harbourmaster_patch_harbour(harbourmaster_user, harbour):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.patch(
        reverse('api:harbour-detail', kwargs={'pk': harbour.id}), {'name': 'Some Harbour'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_patch_harbour(secretary_user, harbour):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.patch(
        reverse('api:harbour-detail', kwargs={'pk': harbour.id}), {'name': 'Some Harbour'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_patch_harbour(committee_member_user, harbour):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.patch(
        reverse('api:harbour-detail', kwargs={'pk': harbour.id}), {'name': 'Some Harbour'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_harbour(ordinary_user, harbour):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(
        reverse('api:harbour-detail', kwargs={'pk': harbour.id}), {'name': 'Some Harbour'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_patch_harbour(harbour):
    client = APIClient()

    response = client.patch(
        reverse('api:harbour-detail', kwargs={'pk': harbour.id}), {'name': 'Some Harbour'}, format='json')
    assert response.status_code == 403


# DELETE

@pytest.mark.django_db()
def test_secretary_delete_harbour(secretary_user, harbour):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.delete(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_harbourmaster_delete_harbour(harbourmaster_user, harbour):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.delete(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_delete_harbour(committee_member_user, harbour):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.delete(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_delete_harbour(ordinary_user, harbour):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.delete(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_delete_harbour(harbour):
    client = APIClient()

    response = client.delete(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    assert response.status_code == 403


# Jetty tests
# GET

@pytest.mark.django_db()
def test_harbourmaster_list_jetties(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:jetty-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_get_jetty(harbourmaster_user, jetty):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_list_jetties(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:jetty-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_get_jetty(secretary_user, jetty):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_list_jetties(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:jetty-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_get_jetty(committee_member_user, jetty):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_list_jetties(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:jetty-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_get_jetty(ordinary_user, jetty):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_unauthenticated_list_jetties():
    client = APIClient()

    response = client.get(reverse('api:jetty-list'))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_jetty(jetty):
    client = APIClient()

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 403


# POST

@pytest.mark.django_db()
def test_harbourmaster_post_jetty(admin_user, harbourmaster_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.post(reverse('api:jetty-list'), {
        'harbour': harbour_url,
        'name': 'Aa'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_post_jetty(admin_user, secretary_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=secretary_user.username, password='password')

    response = client.post(reverse('api:jetty-list'), {
        'harbour': harbour_url,
        'name': 'Aa'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_post_jetty(admin_user, committee_member_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=committee_member_user.username, password='password')

    response = client.post(reverse('api:jetty-list'), {
        'harbour': harbour_url,
        'name': 'Aa'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_post_jetty(admin_user, ordinary_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=ordinary_user.username, password='password')

    response = client.post(reverse('api:jetty-list'), {
        'harbour': harbour_url,
        'name': 'Aa'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_post_jetty(admin_user, harbour):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:harbour-detail', kwargs={'pk': harbour.id}))
    harbour_url = json.loads(response.content.decode('utf-8'))['url']

    client.logout()

    response = client.post(reverse('api:jetty-list'), {
        'harbour': harbour_url,
        'name': 'Aa'
    }, format='json')
    assert response.status_code == 403


# PUT

@pytest.mark.django_db()
def test_harbourmaster_put_jetty(admin_user, harbourmaster_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_content = json.loads(response.content.decode('utf-8'))
    del jetty_content['url']
    del jetty_content['berths']

    assert client.login(username=harbourmaster_user.username, password='password')

    jetty_content['name'] = 'Aa'
    response = client.put(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), jetty_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_put_jetty(admin_user, secretary_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_content = json.loads(response.content.decode('utf-8'))
    del jetty_content['url']
    del jetty_content['berths']

    assert client.login(username=secretary_user.username, password='password')

    jetty_content['name'] = 'Aa'
    response = client.put(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), jetty_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_put_jetty(admin_user, committee_member_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_content = json.loads(response.content.decode('utf-8'))
    del jetty_content['url']
    del jetty_content['berths']

    assert client.login(username=committee_member_user.username, password='password')

    jetty_content['name'] = 'Aa'
    response = client.put(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), jetty_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_jetty(admin_user, ordinary_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_content = json.loads(response.content.decode('utf-8'))
    del jetty_content['url']
    del jetty_content['berths']

    assert client.login(username=ordinary_user.username, password='password')

    jetty_content['name'] = 'Aa'
    response = client.put(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), jetty_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_put_jetty(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_content = json.loads(response.content.decode('utf-8'))
    del jetty_content['url']
    del jetty_content['berths']

    client.logout()

    jetty_content['name'] = 'Aa'
    response = client.put(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), jetty_content, format='json')
    assert response.status_code == 403


# PATCH

@pytest.mark.django_db()
def test_harbourmaster_patch_jetty(harbourmaster_user, jetty):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.patch(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), {'name': 'Some Jetty'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_patch_jetty(secretary_user, jetty):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.patch(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), {'name': 'Some Jetty'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_patch_jetty(committee_member_user, jetty):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.patch(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), {'name': 'Some Jetty'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_jetty(ordinary_user, jetty):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), {'name': 'Some Jetty'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_patch_jetty(jetty):
    client = APIClient()

    response = client.patch(reverse('api:jetty-detail', kwargs={'pk': jetty.id}), {'name': 'Some Jetty'}, format='json')
    assert response.status_code == 403


# DELETE

@pytest.mark.django_db()
def test_secretary_delete_jetty(secretary_user, jetty):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.delete(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_harbourmaster_delete_jetty(harbourmaster_user, jetty):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.delete(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_delete_jetty(committee_member_user, jetty):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.delete(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_delete_jetty(ordinary_user, jetty):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.delete(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_delete_jetty(jetty):
    client = APIClient()

    response = client.delete(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    assert response.status_code == 403


# Berth tests
# GET

@pytest.mark.django_db()
def test_harbourmaster_list_berths(harbourmaster_user):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:berth-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_harbourmaster_get_berth(harbourmaster_user, berth):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_list_berths(secretary_user):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:berth-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_get_berth(secretary_user, berth):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_list_berths(committee_member_user):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:berth-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_committee_member_get_berth(committee_member_user, berth):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_list_berths(ordinary_user):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:berth-list'))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_ordinary_user_get_berth(ordinary_user, berth):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 200


@pytest.mark.django_db()
def test_unauthenticated_list_berths():
    client = APIClient()

    response = client.get(reverse('api:berth-list'))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_get_berth(berth):
    client = APIClient()

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 403


# POST

@pytest.mark.django_db()
def test_harbourmaster_post_berth(admin_user, harbourmaster_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.post(reverse('api:berth-list'), {
        'jetty': jetty_url,
        'name': '03'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_post_berth(admin_user, secretary_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=secretary_user.username, password='password')

    response = client.post(reverse('api:berth-list'), {
        'jetty': jetty_url,
        'name': '03'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_post_berth(admin_user, committee_member_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=committee_member_user.username, password='password')

    response = client.post(reverse('api:berth-list'), {
        'jetty': jetty_url,
        'name': '03'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_post_berth(admin_user, ordinary_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=ordinary_user.username, password='password')

    response = client.post(reverse('api:berth-list'), {
        'jetty': jetty_url,
        'name': '03'
    }, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_post_berth(admin_user, jetty):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:jetty-detail', kwargs={'pk': jetty.id}))
    jetty_url = json.loads(response.content.decode('utf-8'))['url']

    client.logout()

    response = client.post(reverse('api:berth-list'), {
        'jetty': jetty_url,
        'name': '03'
    }, format='json')
    assert response.status_code == 403


# PUT

@pytest.mark.django_db()
def test_harbourmaster_put_berth_name(admin_user, harbourmaster_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    berth_content['name'] = '03'
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_harbourmaster_put_berth_boat(admin_user, harbourmaster_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    berth_content['boat'] = boat_url
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_put_berth_name(admin_user, secretary_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    assert client.login(username=secretary_user.username, password='password')

    berth_content['name'] = '03'
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_put_berth_boat(admin_user, secretary_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    assert client.login(username=secretary_user.username, password='password')

    berth_content['boat'] = boat_url
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_put_berth_name(admin_user, committee_member_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    assert client.login(username=committee_member_user.username, password='password')

    berth_content['name'] = '03'
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_put_berth_boat(admin_user, committee_member_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    assert client.login(username=committee_member_user.username, password='password')

    berth_content['boat'] = boat_url
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_berth_name(admin_user, ordinary_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    assert client.login(username=ordinary_user.username, password='password')

    berth_content['name'] = '03'
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_put_berth_boat(admin_user, ordinary_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    assert client.login(username=ordinary_user.username, password='password')

    berth_content['boat'] = boat_url
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_put_berth_name(admin_user, berth):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    client.logout()

    berth_content['name'] = '03'
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_put_berth_boat(admin_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    response = client.get(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    berth_content = json.loads(response.content.decode('utf-8'))
    del berth_content['url']

    client.logout()

    berth_content['boat'] = boat_url
    response = client.put(reverse('api:berth-detail', kwargs={'pk': berth.id}), berth_content, format='json')
    assert response.status_code == 403


# PATCH

@pytest.mark.django_db()
def test_harbourmaster_patch_berth_name(harbourmaster_user, berth):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'name': 'Some Berth'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_harbourmaster_patch_berth_boat(admin_user, harbourmaster_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'boat': boat_url}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db()
def test_secretary_patch_berth_name(secretary_user, berth):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'name': 'Some Berth'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_secretary_patch_berth_boat(admin_user, secretary_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=secretary_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'boat': boat_url}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_patch_berth_name(committee_member_user, berth):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'name': 'Some Berth'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_patch_berth_boat(admin_user, committee_member_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=committee_member_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'boat': boat_url}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_berth_name(ordinary_user, berth):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'name': 'Some Berth'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_patch_berth_boat(admin_user, ordinary_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    assert client.login(username=ordinary_user.username, password='password')

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'boat': boat_url}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_patch_berth_name(berth):
    client = APIClient()

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'name': 'Some Berth'}, format='json')
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthorized_patch_berth_boat(admin_user, berth, boat):
    client = APIClient()
    assert client.login(username=admin_user.username, password='password')

    response = client.get(reverse('api:boat-detail', kwargs={'pk': boat.id}))
    boat_url = json.loads(response.content.decode('utf-8'))['url']

    client.logout()

    response = client.patch(reverse('api:berth-detail', kwargs={'pk': berth.id}), {'boat': boat_url}, format='json')
    assert response.status_code == 403


# DELETE

@pytest.mark.django_db()
def test_secretary_delete_berth(secretary_user, berth):
    client = APIClient()
    assert client.login(username=secretary_user.username, password='password')

    response = client.delete(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_harbourmaster_delete_berth(harbourmaster_user, berth):
    client = APIClient()
    assert client.login(username=harbourmaster_user.username, password='password')

    response = client.delete(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_committee_member_delete_berth(committee_member_user, berth):
    client = APIClient()
    assert client.login(username=committee_member_user.username, password='password')

    response = client.delete(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_ordinary_user_delete_berth(ordinary_user, berth):
    client = APIClient()
    assert client.login(username=ordinary_user.username, password='password')

    response = client.delete(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 403


@pytest.mark.django_db()
def test_unauthenticated_delete_berth(berth):
    client = APIClient()

    response = client.delete(reverse('api:berth-detail', kwargs={'pk': berth.id}))
    assert response.status_code == 403

