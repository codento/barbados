from rest_framework.test import APIClient
import pytest
import json

from barbados.barbadosdb import tests


@pytest.fixture
def admin_user():
    user = tests.UserFactory.create()
    user.is_superuser = True
    user.password = 'password'
    user.save()
    return user


@pytest.mark.django_db()
def test_get_club(admin_user):
    club = tests.ClubFactory.create()
    client = APIClient()
    client.login(username=admin_user.username, password='password')
    response = client.get('/api/club/')
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    assert len(content) == 1
    assert content[0]['name'] == club.name

