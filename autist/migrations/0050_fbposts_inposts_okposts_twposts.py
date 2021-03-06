# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-02 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('autist', '0049_remove_vkposts_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='FbPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', tinymce.models.HTMLField(blank=True, verbose_name='Текст записи')),
            ],
        ),
        migrations.CreateModel(
            name='InPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', tinymce.models.HTMLField(blank=True, verbose_name='Текст записи')),
            ],
        ),
        migrations.CreateModel(
            name='OkPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', tinymce.models.HTMLField(blank=True, verbose_name='Текст записи')),
            ],
        ),
        migrations.CreateModel(
            name='TwPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', tinymce.models.HTMLField(blank=True, verbose_name='Текст записи')),
            ],
        ),
    ]
