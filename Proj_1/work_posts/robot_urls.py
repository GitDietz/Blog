from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.robot_list, name='robot_list'),
    url(r'^create/$', views.robot_create, name='robot_create'),
    url(r'^(?P<id>\d+)/$', views.robot_detail, name = 'robot_detail'),
    # url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name = 'detail'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name = 'update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete),
]


