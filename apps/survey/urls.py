from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',
    url(r'^profile/$', views.profile_index, name='survey_profile'),
    url(r'^main/$', views.main_index),
    url(r'^group_management/$', views.group_management, name='group_management'),
    url(r'^run/(?P<shortname>.+)/$', views.run_index, name='survey_run'),
    url(r'^thanks/(?P<shortname>.+)/$', views.thanks_run, name='survey_run_thanks'),
    url(r'^thanks_profile/$', views.thanks_profile, name='profile_thanks'),
    url(r'^people/add/$', views.people_add, name='survey_people_add'),
    url(r'^people/edit/$', views.people_edit, name='survey_people_edit'),
    url(r'^people/remove/$', views.people_remove, name='survey_people_remove'),
    url(r'^select/$', views.select_user, name='survey_select_user'),
    url(r'^$', views.index, name='survey_index'),
)

