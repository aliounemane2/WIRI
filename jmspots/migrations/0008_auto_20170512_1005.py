# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-12 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jmspots', '0007_auto_20170512_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        # migrations.AddField(
        #     model_name='institution',
        #     name='date_begin',
        #     field=models.DateTimeField(),
        # ),
        # migrations.AddField(
        #     model_name='institution',
        #     name='date_end',
        #     field=models.DateTimeField(),
        # ),
    ]
