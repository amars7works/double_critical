# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-03-26 15:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UGC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ugc_title', models.CharField(max_length=30)),
                ('like_count', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UGCComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ugc_comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game')),
                ('ugc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.UGC')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UGCCommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game')),
                ('ugc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.UGC')),
                ('ugccomment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.UGCComment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UGCLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_type', models.CharField(choices=[('+1', 'LIKE'), ('-1', 'DISLIKE'), ('0', 'NEUTRAL')], default='0', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('ugc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.UGC')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UGCReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('ugc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.UGC')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='ugcreport',
            unique_together=set([('user', 'ugc')]),
        ),
        migrations.AlterUniqueTogether(
            name='ugclike',
            unique_together=set([('user', 'ugc')]),
        ),
        migrations.AlterUniqueTogether(
            name='ugccommentlike',
            unique_together=set([('user', 'ugccomment', 'game', 'ugc')]),
        ),
        migrations.AlterUniqueTogether(
            name='ugccomment',
            unique_together=set([('user', 'game', 'ugc')]),
        ),
        migrations.AlterUniqueTogether(
            name='ugc',
            unique_together=set([('user', 'game', 'ugc_title')]),
        ),
    ]
