# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-06 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jmspots', '0002_card_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercard',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
