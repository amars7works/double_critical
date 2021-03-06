# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-06-13 07:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Designer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designer_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='GameFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_title', models.CharField(max_length=30)),
                ('game_comment', models.TextField(blank=True, null=True)),
                ('game_description', models.CharField(max_length=250)),
                ('like_count', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mechanism',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mechanism', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisher_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='data',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='scan_type',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='gamecategory',
            name='status',
            field=models.CharField(choices=[('review', 'REVIEW'), ('published', 'PUBLISHED')], default='review', max_length=10),
        ),
        migrations.RemoveField(
            model_name='game',
            name='artist',
        ),
        migrations.AddField(
            model_name='game',
            name='artist',
            field=models.ManyToManyField(to='game.Artist'),
        ),
        migrations.RemoveField(
            model_name='game',
            name='designer',
        ),
        migrations.AddField(
            model_name='game',
            name='designer',
            field=models.ManyToManyField(to='game.Designer'),
        ),
        migrations.RemoveField(
            model_name='game',
            name='mechanism',
        ),
        migrations.AddField(
            model_name='game',
            name='mechanism',
            field=models.ManyToManyField(to='game.Mechanism'),
        ),
        migrations.RemoveField(
            model_name='game',
            name='publisher',
        ),
        migrations.AddField(
            model_name='game',
            name='publisher',
            field=models.ManyToManyField(to='game.Publisher'),
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='gamecategory',
            unique_together=set([('category_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='publisher',
            unique_together=set([('publisher_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='mechanism',
            unique_together=set([('mechanism',)]),
        ),
        migrations.AddField(
            model_name='gamefeed',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game'),
        ),
        migrations.AddField(
            model_name='gamefeed',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='designer',
            unique_together=set([('designer_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='artist',
            unique_together=set([('artist_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='gamefeed',
            unique_together=set([('user', 'game', 'game_title')]),
        ),
    ]
