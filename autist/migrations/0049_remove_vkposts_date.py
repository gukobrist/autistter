# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-27 14:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autist', '0048_delete_vk_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vkposts',
            name='date',
        ),
    ]