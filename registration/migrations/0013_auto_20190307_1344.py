# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-03-07 13:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20190306_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sociallogin',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='sociallogin',
            name='family_name',
        ),
        migrations.RemoveField(
            model_name='sociallogin',
            name='given_name',
        ),
        migrations.RemoveField(
            model_name='sociallogin',
            name='name',
        ),
        migrations.AlterField(
            model_name='sociallogin',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
