from django.conf.urls.defaults import *

from . import views

urlpatterns = patterns('',
        url(r'^$', views.form, name='cohort_form'),
        url(r'^register/$', views.register, name='cohort_register'),
)