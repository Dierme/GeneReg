# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-16 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pylab', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='names',
            old_name='question_text',
            new_name='name',
        ),
    ]
