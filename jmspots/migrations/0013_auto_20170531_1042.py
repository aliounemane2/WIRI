# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jmspots', '0012_auto_20170531_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horaires',
            name='days',
            field=models.CharField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'), ('Dimanche', 'Dimanche')], max_length=10),
        ),
    ]