# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-04-02 11:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=5)),
                ('country_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('state', models.CharField(max_length=5)),
                ('provinence', models.CharField(blank=True, max_length=25, null=True)),
                ('country', models.CharField(max_length=5)),
                ('otp', models.CharField(blank=True, max_length=4, null=True)),
                ('terms_conditions', models.BooleanField(default=False)),
                ('newsletter', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SocialLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_client_id', models.CharField(max_length=250, null=True)),
                ('facebook_client_id', models.CharField(max_length=250, null=True)),
                ('google_refresh_token', models.TextField(blank=True, null=True)),
                ('facebook_refresh_token', models.TextField(blank=True, null=True)),
                ('google_access_token', models.TextField(blank=True, null=True)),
                ('facebook_access_token', models.TextField(blank=True, null=True)),
                ('google_id_token', models.TextField(blank=True, null=True)),
                ('access_token_expiry', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=20)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.Country')),
            ],
        ),
    ]
