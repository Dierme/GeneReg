# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_url', models.CharField(max_length=255)),
                ('rating', models.IntegerField()),
            ],
        ),
    ]
