# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0005_remove_testrequest_log_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrequest',
            name='log_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
