# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-26 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_auto_20160726_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentrevision',
            name='revision_number',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
