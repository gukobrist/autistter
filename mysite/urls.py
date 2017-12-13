# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from . import settings
admin.autodiscover()

urlpatterns = [

	url(r'^accounts/', include('allauth.urls')),
	url(r'', include('autist.urls')),
	url(r'^ckeditor/', include('ckeditor_uploader.urls')),
	url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)