# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 10:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0007_testrequest_highlighted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Snippet',
        ),
    ]
