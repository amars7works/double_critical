# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-02-08 11:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bgg', '0004_auto_20190208_1036'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='gameextend',
            unique_together=set([('game',)]),
        ),
    ]
