# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-23 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verticals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vertical',
            name='identifier',
            field=models.SlugField(default='default'),
            preserve_default=False,
        ),
    ]
