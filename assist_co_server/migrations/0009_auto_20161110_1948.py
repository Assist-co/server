# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 19:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assist_co_server', '0008_auto_20161110_1919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gender',
            old_name='option_id',
            new_name='sort',
        ),
        migrations.RenameField(
            model_name='profession',
            old_name='option_id',
            new_name='sort',
        ),
        migrations.RenameField(
            model_name='tasktype',
            old_name='option_id',
            new_name='sort',
        ),
    ]
