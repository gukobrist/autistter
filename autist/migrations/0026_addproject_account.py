# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-20 13:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
        ('autist', '0025_remove_addproject_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='addproject',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='socialaccount.SocialAccount'),
            preserve_default=False,
        ),
    ]
