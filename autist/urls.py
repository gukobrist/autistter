# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from .decorators import check_recaptcha

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<slug>[^//]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<slug>[^//]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^about/$', views.page_about, name='page_about'),
    url(r'^contact/$', check_recaptcha(views.page_contact), name='page_contact'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^post_in_vk/$', views.post_in_vk, name='post_in_vk'),
    url(r'^connect_accounts/$', views.page_connect_accounts, name='connect_accounts'),
    url(r'^projects/$', views.page_add_project, name='projects'),
    url(r'^projects/(?P<pk>[^//]+)/edit/$', views.page_edit_project, name='project_edit'),
    url(r'^projects/(?P<pk>[^//]+)/delete/$$', views.project_delete, name='projects_delete'),
    url(r'^example', views.page_example, name='page_example'),
]