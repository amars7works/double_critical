# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-05-07 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20190507_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='category',
        ),
        migrations.AddField(
            model_name='game',
            name='category',
            field=models.ManyToManyField(to='game.GameCategory'),
        ),
    ]
