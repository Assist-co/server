# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assist_co_server', '0005_client_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed_on',
            field=models.DateTimeField(null=True),
        ),
    ]