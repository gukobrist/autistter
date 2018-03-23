# -*- coding: utf-8 -*-
from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone
from allauth.account.forms import BaseSignupForm
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from uuslug import slugify
from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialLogin
from django.db import models
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey(User, related_name='blog_posts')
    title = models.CharField(max_length=250)
    slug = models.CharField(verbose_name='Alias', max_length=250, unique_for_date='published_date')
    text = RichTextUploadingField(blank=True, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    seo_title = models.CharField('TITLE', blank=True, max_length=250)
    seo_description = models.CharField('DESCRIPTION', blank=True, max_length=250)
    seo_keywords = models.CharField('KEYWORDS', blank=True, max_length=250)
    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

class AddProject(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200, verbose_name=u"Назние проекта")
    accounts = models.ManyToManyField(SocialAccount, verbose_name=('Подключенные аккаунты к учетной записи'))

    def __str__(self):
        return self.title


class VkPosts(models.Model):
    text = HTMLField(verbose_name=u'Текст записи', blank=True)

class FbPosts(models.Model):
    text = HTMLField(verbose_name=u'Текст записи', blank=True)

class TwPosts(models.Model):
    text = HTMLField(verbose_name=u'Текст записи', blank=True)

class OkPosts(models.Model):
    text = HTMLField(verbose_name=u'Текст записи', blank=True)

class InPosts(models.Model):
    text = HTMLField(verbose_name=u'Текст записи', blank=True)

class Tasks(models.Model):
    task = models.CharField(max_length=100, verbose_name="Выберите задание")
    link = models.URLField(max_length=100, verbose_name="Ссылка")
    name = models.CharField(max_length=200, verbose_name="Название")
    coasts = models.CharField(max_length=100, verbose_name="Цена")




