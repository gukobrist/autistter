# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-22 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
        ('autist', '0027_remove_addproject_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproject',
            name='connected_accounts',
            field=models.ManyToManyField(to='socialaccount.SocialAccount'),
        ),
    ]
