# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 09:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0004_auto_20170530_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 31, 9, 2, 49, 18680)),
        ),
    ]