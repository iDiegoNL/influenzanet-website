from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from . import views

urlpatterns = patterns('',

    url(r'^$', views.admin_index, name="swauth_admin_index")
)

