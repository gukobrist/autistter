# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-22 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autist', '0030_auto_20180122_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproject',
            name='connected_accounts',
            field=models.ManyToManyField(blank=True, to='socialaccount.SocialAccount', verbose_name='Присоединенные аккаунты'),
        ),
    ]