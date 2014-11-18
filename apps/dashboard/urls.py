from django.conf.urls.defaults import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='dashboard_index'),
    url(r'^badges/$', views.badges, name='dashboard_badges'),
    url(r'^badges/disable/$', views.badge_disable, name='dashboard_badges_disable'),
    url(r'^badges/activate/$', views.badge_activate, name='dashboard_badges_activate'),
    url(r'^chart/1/$', 'django.views.generic.simple.direct_to_template', {'template': 'dashboard/user_charts.html'}, name='dashboard_badges_chart'),
)