# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-02-04 08:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_profile_provinence'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='country',
            name='country_code',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='country',
            name='country_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='country', to='registration.Country'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='registration.State'),
        ),
    ]
