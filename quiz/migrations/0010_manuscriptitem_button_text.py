# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-12 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20170304_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='manuscriptitem',
            name='button_text',
            field=models.TextField(blank=True, default=''),
        ),
    ]
