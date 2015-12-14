# vim: fenc=utf-8

from django.contrib.auth import models as auth_models
from django.core.management.base import CommandError
from barbados.barbadosdb import tests
from django.conf import settings
from django.db import transaction
from django_docopt_command.command import DocOptCommand


class Command(DocOptCommand):
    """A management command to help us test permissions irl
    """

    docs = """Usage: create-test-users [--traceback] [--verbosity=<n>] [--database=<db>]

Options:
    --traceback         Show traceback
    --verbosity=<n>     Verbosity level 0-2
    --database=<db>     Database to use [default: default]
    """

    def handle_docopt(self, arguments):
        if not settings.DEBUG:
            raise CommandError('Run this only in development')

        def make_superuser(user):
            user.is_superuser = True

        users = {'harbourmaster': ('Harbourmaster',),
                 'secretary': ('Membership secretary',),
                 'admin': make_superuser,
                 'user': None}

        with transaction.atomic(using=arguments['--database']):
            for username, todo in users.items():
                u = tests.UserFactory.create()

                u.is_staff = True
                u.username = username

                if isinstance(todo, tuple):
                    gs = auth_models.Group.objects.filter(name__in=todo)
                    for g in gs:
                        u.groups.add(g)
                elif callable(todo):
                    todo(u)

                u.set_password('password')

                u.save()

        print('Created users ({}) with password "password"'.format(', '.join(sorted(users.keys()))))

