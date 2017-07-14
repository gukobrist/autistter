from django.contrib import admin
from .models import Post
from metatags.admin import MetaTagInline

admin.site.register(Post)

class CustomModelAdmin(admin.ModelAdmin):
	inlines = (MetaTagInline,)

# Register your models here.
