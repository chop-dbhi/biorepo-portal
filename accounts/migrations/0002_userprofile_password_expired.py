# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-19 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='password_expired',
            field=models.BooleanField(default=False),
        ),
    ]
