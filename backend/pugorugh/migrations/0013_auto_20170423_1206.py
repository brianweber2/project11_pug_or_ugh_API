# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-04-23 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0012_auto_20170423_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(default='b, y, a, s', max_length=1),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(default='m, f', max_length=1),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=models.CharField(default='s, m, l, xl', max_length=2),
        ),
    ]