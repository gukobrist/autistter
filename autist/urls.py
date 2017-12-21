# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<slug>[^//]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<slug>[^//]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^about', views.page_about, name='page_about'),
    url(r'^contact', views.page_contact, name='page_contact'),
]