# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-06 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0023_auto_20170906_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manuscript',
            name='name',
            field=models.TextField(blank=True, default='', help_text='Used both for admin display and user display when type=voting guide or type=quiz', unique=True),
        ),
    ]