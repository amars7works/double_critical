# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-03-29 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20190329_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='dislike_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='like_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='views',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
