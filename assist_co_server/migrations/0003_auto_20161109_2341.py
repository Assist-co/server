# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-09 23:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assist_co_server', '0002_auto_20161109_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='primary_assistant',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='assist_co_server.Assistant'),
        ),
    ]