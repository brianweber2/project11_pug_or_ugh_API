# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-04-18 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0009_auto_20170418_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(choices=[('l', 'liked'), ('d', 'disliked'), ('u', 'undecided')], default='u', max_length=1),
        ),
    ]
