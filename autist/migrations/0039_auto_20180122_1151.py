# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-22 11:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autist', '0038_auto_20180122_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addproject',
            name='accounts',
        ),
        migrations.RemoveField(
            model_name='addproject',
            name='user',
        ),
        migrations.DeleteModel(
            name='AddProject',
        ),
    ]
