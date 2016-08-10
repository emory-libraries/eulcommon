# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('object_id', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('task_id', models.CharField(max_length=100)),
                ('task_start', models.DateTimeField(blank=True, null=True)),
                ('task_end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
