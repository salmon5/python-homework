# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-06-14 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20180614_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablespace',
            name='free_size',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='tablespace',
            name='total_size',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='tablespace',
            name='used_size',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]