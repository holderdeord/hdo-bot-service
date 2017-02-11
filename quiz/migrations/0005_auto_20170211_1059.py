# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-11 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20170211_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manuscriptitem',
            name='promises',
        ),
        migrations.AddField(
            model_name='manuscript',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='manuscript',
            name='promises',
            field=models.ManyToManyField(blank=True, to='quiz.Promise'),
        ),
    ]
