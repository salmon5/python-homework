# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-06-14 06:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20180612_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='tablespace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64)),
                ('total_size', models.CharField(blank=True, max_length=64)),
                ('free_size', models.CharField(blank=True, max_length=64)),
                ('used_size', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='host',
            name='appcompany',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.AppCompany', verbose_name='厂商'),
        ),
        migrations.AlterField(
            model_name='host',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Business', verbose_name='业务系统名称'),
        ),
        migrations.AlterField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.IDC', verbose_name='机房'),
        ),
    ]