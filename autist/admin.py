# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Post, Comment
from metatags.admin import MetaTagInline


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_date', 'status')
    list_filter = ('status', 'created_date', 'published_date', 'author')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ['status', 'published_date']


admin.site.register(Post, PostAdmin)


class CustomModelAdmin(admin.ModelAdmin):
	inlines = (MetaTagInline,)