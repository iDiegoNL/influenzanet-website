from django.conf.urls.defaults import *
from django.conf import settings
from . import views

WAIT_LAUNCH = getattr(settings,'SURVEY_WAIT_LAUNCH', False)

urlpatterns = patterns('',
    url(r'^profile/$', views.wait_launch if WAIT_LAUNCH else views.profile_index, name='survey_profile'),
    url(r'^thanks/$', views.thanks, name='survey_thanks'),
    url(r'^run/(?P<shortname>.+)/$', views.wait_launch if WAIT_LAUNCH else views.run_index, name='survey_run'),
    url(r'^thanks/(?P<shortname>.+)/$', views.thanks_run, name='survey_run_thanks'),
    url(r'^thanks_profile/$', views.thanks_profile, name='profile_thanks'),
    url(r'^people/$', views.people, name='survey_people'),
    url(r'^people/add/$', views.people_add, name='survey_people_add'),
    url(r'^people/edit/$', views.people_edit, name='survey_people_edit'),
    url(r'^people/remove/$', views.people_remove, name='survey_people_remove'),
    url(r'^select/$', views.select_user, name='survey_select_user'),
    url(r'^$', views.wait_launch if WAIT_LAUNCH else views.index, name='survey_index'),
)

