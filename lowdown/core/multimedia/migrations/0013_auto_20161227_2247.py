# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-27 22:47
from __future__ import unicode_literals

import lowdown.core.verticals.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0012_remove_multimediaimage_vertical'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multimedia',
            name='vertical',
            field=lowdown.core.verticals.fields.VerticalField(choices=[('theprate', 'The Prate'), ('thedrab', 'The Drab')], max_length=32),
        ),
    ]
