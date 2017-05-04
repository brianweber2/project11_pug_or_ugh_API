# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-04-23 22:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0015_auto_20170423_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='breed',
            field=models.CharField(default='Unknown mix', max_length=255),
        ),
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female'), ('u', 'unknown')], max_length=1),
        ),
        migrations.AlterField(
            model_name='dog',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dog',
            name='size',
            field=models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large'), ('u', 'unknown')], max_length=2),
        ),
        migrations.AlterField(
            model_name='userdog',
            name='dog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pugorugh.Dog'),
        ),
    ]