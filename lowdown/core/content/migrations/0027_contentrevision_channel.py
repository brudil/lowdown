# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-08 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0026_auto_20171127_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentrevision',
            name='channel',
            field=models.CharField(default='MAIN', max_length=12),
        ),
    ]
