# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-02-08 10:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bgg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RateGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_rating', models.CharField(choices=[('love', 'LOVE'), ('like', 'LIKE'), ('dislike', 'DISLIKE'), ('hate', 'HATE')], default=None, max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UGC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ugc_title', models.CharField(max_length=30)),
                ('like_count', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UGCComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ugc_comments', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UGCCommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('ugc_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bgg.UGCComment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UGCLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_type', models.CharField(choices=[('+1', 'LIKE'), ('-1', 'DISLIKE'), ('0', 'NEUTRAL')], default='0', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('ugc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bgg.UGC')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='gameextend',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='gameextend',
            name='game',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='bgg.Game'),
        ),
        migrations.AddField(
            model_name='gameextend',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='hotornot',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='game',
            name='extend',
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='ugccomment',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bgg.Game'),
        ),
        migrations.AddField(
            model_name='ugccomment',
            name='ugc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bgg.UGC'),
        ),
        migrations.AddField(
            model_name='ugccomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rategame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bgg.Game'),
        ),
        migrations.AddField(
            model_name='rategame',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gamecollection',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bgg.Game'),
        ),
        migrations.AddField(
            model_name='gamecollection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='followgame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bgg.Game'),
        ),
        migrations.AddField(
            model_name='followgame',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='ugclike',
            unique_together=set([('user', 'ugc')]),
        ),
        migrations.AlterUniqueTogether(
            name='ugccommentlike',
            unique_together=set([('user', 'ugc_comment')]),
        ),
        migrations.AlterUniqueTogether(
            name='ugccomment',
            unique_together=set([('user', 'game', 'ugc')]),
        ),
        migrations.AlterUniqueTogether(
            name='ugc',
            unique_together=set([('user', 'ugc_title')]),
        ),
        migrations.AlterUniqueTogether(
            name='rategame',
            unique_together=set([('user', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='gamecollection',
            unique_together=set([('user', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='followuser',
            unique_together=set([('follower', 'following')]),
        ),
        migrations.AlterUniqueTogether(
            name='followgame',
            unique_together=set([('user', 'game')]),
        ),
    ]
