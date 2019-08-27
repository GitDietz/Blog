from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name='list'),
    url(r'^create/$', views.post_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name = 'detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name = 'update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete),
]

# urlpatterns = [
#     url(r'^$', views.post_list, name='list'),
#     url(r'^create/$', views.post_create),   #this is equivalent to the below below to be depricated
#     #url(r'^create/$', "work_posts.views.post_create"), # this includes the urls file under the work_post folder
#     #url(r'^detail/$', views.post_detail),
#     url(r'^(?P<id>\d+)/$', views.post_detail, name = 'detail'),
#     #url(r'^update/$', views.post_update),
#     url(r'^(?P<id>\d+)/edit/$', views.post_update, name = 'update'),
#     url(r'^(?P<id>\d+)/delete/$', views.post_delete),
# ]
