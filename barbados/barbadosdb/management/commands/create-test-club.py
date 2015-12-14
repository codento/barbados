# vim: fenc=utf-8

from django.core.management.base import CommandError
from barbados.barbadosdb import models, tests
from django.conf import settings
from django.db import transaction
from django_docopt_command.command import DocOptCommand


class Command(DocOptCommand):
    """A management command for creating a club and its hierarchy
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

        users = models.User.objects.all()

        # See if we have critical users
        harbourmaster = None
        secretary = None
        admin = None
        user = None

        for user in users:
            if user.username == 'harbourmaster':
                harbourmaster = user
            elif user.username == 'secretary':
                secretary = user
            elif user.username == 'admin':
                admin = user
            elif user.username == 'user':
                user = user

        with transaction.atomic(using=arguments['--database']):
            berth = tests.BerthFactory.create()

            jetty = berth.jetty
            harbour = jetty.harbour
            club = harbour.club

            for i in range(19):
                tests.BerthFactory.create(jetty=jetty)

            other_jetty = tests.JettyFactory.create(harbour=harbour)

            for i in range(20):
                tests.BerthFactory.create(jetty=other_jetty)

            print('Created {} and its minion data'.format(club))

            # This is not totally valid but good enough to test, or especially
            # warm up the database
            if harbourmaster:
                models.Membership.objects.create(club=club, user=harbourmaster)

            if secretary:
                models.Membership.objects.create(club=club, user=secretary)

            if admin:
                models.Membership.objects.create(club=club, user=admin)

            if user:
                models.Membership.objects.create(club=club, user=user)

