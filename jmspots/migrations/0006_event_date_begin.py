# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-12 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jmspots', '0005_remove_event_date_begin'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date_begin',
            field=models.DateField(),
        ),
    ]