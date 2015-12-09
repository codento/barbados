# vim: fenc=utf-8

from . import models

import pytest

# Create your tests here.


@pytest.mark.django_db
def test_bad_phone_number():
    __tracebackhide__ = True

    try:
        u = models.User(username='jkala',
                        email='james.kala@example.com',
                        phone_number='123')

        u.full_clean()

        pytest.fail(msg='User should not be valid')
    except models.ValidationError:
        pass

