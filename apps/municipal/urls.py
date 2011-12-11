# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',
    url(r'^search', views.search, name='search'),
)