# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodset',
            name='time',
            field=models.CharField(max_length=10),
        ),
    ]