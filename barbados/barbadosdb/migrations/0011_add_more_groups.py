# -*- coding: utf-8 -*-
# Generated by hand
from __future__ import unicode_literals

from django.db import migrations


def create_group(apps, schema_editor):
    """Go with this instead of fixtures
    """

    Group = apps.get_model('auth', 'Group')
    Group.objects.create(name='Member')


class Migration(migrations.Migration):

    dependencies = [
        ('barbadosdb', '0010_add_view_perms'),
    ]

    operations = [
        migrations.RunPython(create_group),
    ]