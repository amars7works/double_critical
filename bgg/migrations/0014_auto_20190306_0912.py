# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-03-06 09:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bgg', '0013_auto_20190305_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gametag',
            name='tag_name',
        ),
        migrations.AddField(
            model_name='gametag',
            name='tag_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bgg.Tags'),
            preserve_default=False,
        ),
    ]
