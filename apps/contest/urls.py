from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.conf import settings

from loginurl.views import cleanup, login

urlpatterns = patterns('apps.contest.views',
    (r'^prijs_grafiek_xml.php', 'prijs_grafiek'), 
    (r'^prijs_weergave_xml.php', 'prijs_weergave'), 
    (r'^relay2.php', 'relay2'), 

    (r'^winners/', 'winners'), 
)

