# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^search', views.search, name='municipal_search'),
    url(r'^title/(?P<code>\d+)$', views.title, name='municipal_title'),
)