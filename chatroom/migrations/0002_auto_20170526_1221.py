# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_mydevice'),
        ('chatroom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='users_receivers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_receive', to='users.User'),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='chatroom/'),
        ),
        migrations.AlterField(
            model_name='message',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='users.User'),
        ),
    ]
