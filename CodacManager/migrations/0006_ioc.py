# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-22 14:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CodacManager', '0005_auto_20160121_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='IOC',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CodacManager.Host')),
            ],
        ),
    ]
