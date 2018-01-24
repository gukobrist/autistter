# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Post
from metatags.admin import MetaTagInline
from django import forms

admin.site.register(Post)


class CustomModelAdmin(admin.ModelAdmin):
	inlines = (MetaTagInline,)