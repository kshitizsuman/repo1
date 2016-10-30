from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^create/$', "posts.views.post_create"),
    url(r'^detail/$', "posts.views.post_detail"),
    url(r'^list/$', "posts.views.post_list"),
    url(r'^update/$', "posts.views.post_update"),
    url(r'^create/$', "posts.views.post_create"),
]