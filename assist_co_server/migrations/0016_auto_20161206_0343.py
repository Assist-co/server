# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 03:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assist_co_server', '0015_auto_20161206_0332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
