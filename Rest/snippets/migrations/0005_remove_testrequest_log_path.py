# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 08:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_auto_20170619_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testrequest',
            name='log_path',
        ),
    ]
