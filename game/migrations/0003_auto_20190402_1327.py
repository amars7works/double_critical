# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-04-02 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20190402_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamecategory',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='id',
        ),
        migrations.AlterField(
            model_name='gamecategory',
            name='category_name',
            field=models.CharField(default='n', max_length=60, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tags',
            name='tag_name',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
