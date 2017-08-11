# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-17 12:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import usasui.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testcase_id', models.CharField(blank=True, max_length=20, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usasui.Project')),
            ],
        ),
        migrations.CreateModel(
            name='TestRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_run_id', models.CharField(default=usasui.models.get_test_id, max_length=50)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('execution', models.DateTimeField(blank=True, null=True)),
                ('test_suit_id', models.CharField(max_length=50)),
                ('test_file', models.FileField(upload_to=b'')),
                ('log_path', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(choices=[('w', 'Waiting'), ('t', 'Testing'), ('c', 'Completed'), ('e', 'Error')], default='w', max_length=10)),
                ('result', models.CharField(blank=True, max_length=30, null=True)),
                ('envt', models.CharField(blank=True, max_length=30, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usasui.Project')),
            ],
        ),
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_run_name', models.CharField(max_length=100)),
                ('result', models.CharField(max_length=20)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usasui.Project')),
                ('test_case', models.ManyToManyField(to='usasui.TestCase')),
                ('test_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usasui.TestRequest')),
            ],
        ),
        migrations.CreateModel(
            name='TestSuit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=12)),
            ],
        ),
        migrations.AddField(
            model_name='testrun',
            name='test_suit_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usasui.TestSuit'),
        ),
        migrations.AddField(
            model_name='testrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='testcase',
            name='test_suit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usasui.TestSuit'),
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
