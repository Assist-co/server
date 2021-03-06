# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assist_co_server', '0007_auto_20161110_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistant',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assist_co_server.Gender'),
        ),
        migrations.AlterField(
            model_name='client',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assist_co_server.Gender'),
        ),
        migrations.AlterField(
            model_name='client',
            name='primary_assistant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assist_co_server.Assistant'),
        ),
        migrations.AlterField(
            model_name='client',
            name='profession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assist_co_server.Profession'),
        ),
        migrations.AlterField(
            model_name='task',
            name='assistant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assist_co_server.Assistant'),
        ),
        migrations.AlterField(
            model_name='task',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assist_co_server.Client'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assist_co_server.TaskType'),
        ),
    ]
