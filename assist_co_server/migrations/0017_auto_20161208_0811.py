# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assist_co_server', '0016_auto_20161206_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assistant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assist_co_server.Assistant'),
        ),
        migrations.AlterField(
            model_name='task',
            name='contacts',
            field=models.ManyToManyField(blank=True, to='assist_co_server.Contact'),
        ),
        migrations.AlterField(
            model_name='task',
            name='end_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
