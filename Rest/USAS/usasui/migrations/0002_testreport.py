# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 15:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usasui', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testrequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rest', to='usasui.TestRequest')),
            ],
        ),
    ]
