# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 14:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_mydevice'),
        ('chatroom', '0003_message_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 30, 14, 44, 34, 132186)),
        ),
        migrations.RemoveField(
            model_name='message',
            name='users_receivers',
        ),
        migrations.AddField(
            model_name='message',
            name='users_receivers',
            field=models.ManyToManyField(related_name='list_receive', to='users.User'),
        ),
    ]
