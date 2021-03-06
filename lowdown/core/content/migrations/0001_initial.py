# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-08 20:41
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('topics', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContentDiscussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_comments', to=settings.AUTH_USER_MODEL)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='content.Content')),
            ],
        ),
        migrations.CreateModel(
            name='ContentEditorialMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'Stub'), (5, 'Writing'), (7, 'Review'), (9, 'Finished')], default=1)),
                ('locked_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('due_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('embargoed_till', models.DateTimeField(blank=True, default=None, null=True)),
                ('revision_count', models.IntegerField(default=0)),
                ('assigned_user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_content', to=settings.AUTH_USER_MODEL)),
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='editorial_metadata', to='content.Content')),
            ],
        ),
        migrations.CreateModel(
            name='ContentRevision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('headline', models.TextField()),
                ('short_headline', models.TextField(blank=True)),
                ('byline_markup', models.TextField(blank=True)),
                ('kicker', models.TextField(blank=True)),
                ('slug', models.CharField(blank=True, max_length=60)),
                ('tone', models.SmallIntegerField(choices=[(1, 'Content'), (2, 'Review'), (3, 'Viewpoint'), (4, 'Storytelling'), (5, 'Interactive'), (6, 'Guide')], db_index=True)),
                ('form', models.SmallIntegerField(choices=[(1, 'Article'), (2, 'Video'), (3, 'Interactive'), (4, 'Gallery')], db_index=True)),
                ('specturm_document', django.contrib.postgres.fields.jsonb.JSONField(blank=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revisions', to='content.Content')),
                ('series', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_revisions', to='series.Series')),
                ('topics', models.ManyToManyField(blank=True, related_name='content_revisions', to='topics.Topic')),
            ],
        ),
        migrations.AddField(
            model_name='contenteditorialmetadata',
            name='current_revision',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='content.ContentRevision'),
        ),
        migrations.AddField(
            model_name='contenteditorialmetadata',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watched_content', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contentdiscussion',
            name='content_revision',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='content.ContentRevision'),
        ),
        migrations.AddField(
            model_name='content',
            name='published_revision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published', to='content.ContentRevision'),
        ),
    ]
