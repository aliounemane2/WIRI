# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-12 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jmspots', '0006_event_date_begin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_begin',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_end',
            field=models.DateTimeField(),
        ),
    ]
