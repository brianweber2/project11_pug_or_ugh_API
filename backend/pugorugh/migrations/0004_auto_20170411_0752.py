# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-04-11 14:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pugorugh', '0003_auto_20170410_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdog',
            name='user',
        ),
        migrations.AddField(
            model_name='userdog',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
