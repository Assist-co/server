# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 03:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assist_co_server', '0010_task_is_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
