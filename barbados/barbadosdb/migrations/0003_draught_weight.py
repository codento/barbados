# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barbadosdb', '0002_bytestrings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boat',
            name='draught',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='boat',
            name='weight',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
