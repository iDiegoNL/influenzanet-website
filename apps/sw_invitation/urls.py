from django.conf.urls.defaults import patterns,url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.invite, name='invite_index'),
    url(r'^preview$', views.preview, name='invite_preview'),                    
)